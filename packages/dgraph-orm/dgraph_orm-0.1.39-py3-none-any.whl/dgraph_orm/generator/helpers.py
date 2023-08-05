from __future__ import annotations

import keyword
import typing as T
import re
import json
from enum import Enum
from pydantic import BaseModel, Field
from black import FileMode, format_str

NODE_CONFIG_NAME = "GQL"
ORM_MODEL_NAME = "GQLInput"
DEFAULT_INDENT = "    "


class NodeConfig(BaseModel):
    node_name: str

    resolver_name: str = None

    # object names
    add_model: str = None
    patch_model: str = None
    ref_model: str = None

    # queries
    get_function_name: str = None
    query_function_name: str = None
    payload_node_name: str = None

    # mutations
    add_function_name: str = None
    update_function_name: str = None
    delete_function_name: str = None

    url: str
    uid_field_name: str

    @classmethod
    def default_from_node_name(cls, node_name: str, url: str) -> NodeConfig:
        return cls(
            node_name=node_name,
            resolver_name=f"{node_name}Resolver",
            get_function_name=f"get{node_name}",
            query_function_name=f"query{node_name}",
            payload_node_name=f"{create_payload_node_name(node_name)}",
            add_function_name=f"add{node_name}",
            update_function_name=f"update{node_name}",
            delete_function_name=f"delete{node_name}",
            add_model=f"Add{node_name}Input",
            patch_model=f"{node_name}Patch",
            ref_model=f"{node_name}Ref",
            url=url,
            uid_field_name="id",
        )

    def create_aggregate(
        self, postfix: str = None, get_function_name: str = None
    ) -> NodeConfig:
        postfix = "AggregateResult" if postfix is None else postfix
        get_function_name = (
            f"aggregate{self.node_name}"
            if get_function_name is None
            else get_function_name
        )
        node_name = f"{self.node_name}{postfix}"
        return self.__class__(
            node_name=node_name,
            url=self.url,
            get_function_name=get_function_name,
            uid_field_name="count",
        )

    @staticmethod
    def str_or_none(s: T.Optional[str], quotes: bool = False) -> str:
        if s is None:
            return "None"
        if quotes:
            s = f'"{s}"'
        return s

    def to_config_class(self) -> str:
        s = f"""
class {NODE_CONFIG_NAME}:
    typename = "{self.node_name}"
    payload_node_name = {self.str_or_none(self.payload_node_name, quotes=True)}
    resolver: Type[{self.str_or_none(self.resolver_name)}]

    # models
    add_model: Type[{self.str_or_none(self.add_model)}] = {self.str_or_none(self.add_model)}
    patch_model: Type[{self.str_or_none(self.patch_model)}] = {self.str_or_none(self.patch_model)}
    ref_model: Type[{self.str_or_none(self.ref_model)}] = {self.str_or_none(self.ref_model)}

    # functions
    get_function_name: str = {self.str_or_none(self.get_function_name, quotes=True)}
    query_function_name: str = {self.str_or_none(self.query_function_name, quotes=True)}

    add_function_name: str = {self.str_or_none(self.add_function_name, quotes=True)}
    update_function_name: str = {self.str_or_none(self.update_function_name, quotes=True)}
    delete_function_name: str = {self.str_or_none(self.delete_function_name, quotes=True)}

    url: str = "{self.url}"
    uid_field_name: str = "{self.uid_field_name}"
        """

        return s


def imports() -> str:
    lines = [
        "from __future__ import annotations",
        "from enum import Enum",
        "from datetime import datetime",
        "from pydantic import BaseModel, Field",
        f"from dgraph_orm import {ORM_MODEL_NAME}, Node, GQLException",
        "from dgraph_orm.resolver import Params, Resolver",
        "from typing import Optional, Set, Type, ClassVar, List",
    ]
    return "\n".join(lines)


scalar_d = {
    "String": "str",
    "Int": "int",
    "Float": "float",
    "Boolean": "bool",
    "ID": "str",
    "Int64": "int",
    "DateTime": "datetime",
}


class IterableType(str, Enum):
    SET = "Set"
    LIST = "List"


def node_from_type(s: str) -> str:
    return s.replace("]", "").replace("[", "").replace("!", "")


def indent_lines(s: str, indent: str = None) -> str:
    chunks = s.split("\n")
    indent = indent or "\t"
    return indent + f"\n{indent}".join(chunks)


class Arg(BaseModel):
    """
    name: filter, type: StudentFilter       name: order, type: StudentOrder
    """

    name: str
    type: str

    @property
    def node_name(self) -> str:
        return node_from_type(self.type)

    def is_node_required(self) -> bool:
        return f"{self.node_name}!" in self.type

    def is_set_required(self) -> bool:
        return "]!" in self.type

    def python_type(self, iterable_type: IterableType = IterableType.LIST) -> str:
        """StudentFilter -> Optional[StudentFilter]"""
        s_or_l = iterable_type.value
        python_type = self.type.replace("[", f"{s_or_l}[")
        if not self.is_set_required():
            if f"{s_or_l}[" in python_type:
                python_type = (
                    python_type.replace(f"{s_or_l}[", f"Optional[{s_or_l}[") + "]"
                )
        if not self.is_node_required():
            python_type = python_type.replace(
                self.node_name, f"Optional[{self.node_name}]"
            )
        if python_scalar := scalar_d.get(self.node_name):
            python_type = python_type.replace(self.node_name, python_scalar)
        python_type = python_type.replace("!", "")
        return python_type

    def should_use_alias(self) -> bool:
        return self.name in keyword.kwlist

    def value(
        self,
        use_field: bool,
        allow_mutation: bool = True,
        iterable_type: IterableType = IterableType.LIST,
    ) -> str:
        """ None, Field(Node), Field(...), Field(..., allow_mutations=False) """
        alias_str = ""
        if use_field and self.should_use_alias():
            alias_str = f' , alias="{self.name}"'
        if self.python_type(iterable_type=iterable_type).startswith("Optional"):
            s = (
                "None"
                if not use_field
                else f"Field(None, allow_mutation={allow_mutation}{alias_str})"
            )
        else:
            s = (
                ""
                if not use_field
                else f"Field(..., allow_mutation={allow_mutation}{alias_str})"
            )
        return s

    def full_line_for_arg(
        self,
        use_field: bool = False,
        allow_mutation: bool = True,
        iterable_type: IterableType = IterableType.LIST,
    ) -> str:
        value_str = ""
        if value := self.value(use_field=use_field, allow_mutation=allow_mutation):
            value_str = f" = {value}"
        name = self.name
        if use_field and self.should_use_alias():
            name = f"{self.name}_"
        return f"{name}: {self.python_type(iterable_type=iterable_type)}{value_str}"

    @classmethod
    def from_str(cls, s) -> T.List[Arg]:
        s = s.strip()
        pattern = r"(\w*):\s([\w\[!\]]*)"
        matches = re.findall(pattern, s)
        args: T.List[cls] = []
        for match in matches:
            name, type = match
            args.append(cls(name=name, type=type))
        return args


class Function(BaseModel):
    name: str
    return_type: str
    args: T.List[Arg]

    class Config:
        anystr_strip_whitespace = True

    @property
    def return_node(self) -> str:
        return node_from_type(self.return_type)

    def return_type_python(
        self,
        remove_optional_set: bool = False,
        iterable_type: IterableType = IterableType.LIST,
    ) -> str:
        s_or_l = iterable_type.value
        python_type = Arg(name="temp", type=self.return_type).python_type(
            iterable_type=iterable_type
        )
        if remove_optional_set:
            """If Sets just return empty then Sets should never be None, so require them to exist"""
            key = f"Optional[{s_or_l}["
            if python_type.startswith(key):
                python_type = python_type.replace(key, f"{s_or_l}[")[:-1]
        return python_type

    @classmethod
    def from_str(cls, s: str) -> T.List[Function]:
        s = s.strip()
        pattern = r"(\w*)\(([^\)]*)\): (.*)"
        func_matches = re.findall(pattern=pattern, string=s)
        node_resolver_functions: T.List[cls] = []
        for match in func_matches:
            name, args_str, return_type = match
            node_resolver_functions.append(
                cls(name=name, args=Arg.from_str(args_str), return_type=return_type)
            )
        return node_resolver_functions

    def is_required_for_node(self) -> bool:
        return self.return_type.endswith("!")


def create_payload_node_name(node_name: str) -> str:
    return node_name[0].lower() + node_name[1:]


class NodeBuilder:
    def __init__(
        self,
        node_str: str,
        node_config: NodeConfig,
        query_str: str,
        all_node_configs: T.List[NodeConfig],
    ):
        self.all_node_configs = all_node_configs
        self.node_str = self.add_parens_to_node_types(
            node_str, node_names=[c.node_name for c in self.all_node_configs]
        )
        self.node_config = node_config
        self.query_str = query_str

        self.node_name = self.node_name_from_node_str(self.node_str)
        self.resolver_name = f"{self.node_name}Resolver"
        self.edge_functions = Function.from_str(self.node_str)

    def build_edge_functions(self) -> str:
        func_str_lst: T.List[str] = []
        for func in self.edge_functions:
            return_resolver = f"{func.return_node}Resolver"
            # Sets should just return Set, not Optional[Set[...
            func_str = f"""
async def {func.name}(self, resolver: {return_resolver} = None, refresh: bool = False, use_stale: bool = False) -> {func.return_type_python(remove_optional_set=True)}:
    return await self.resolve(name="{func.name}", resolver=resolver, refresh=refresh, use_stale=use_stale)
            """
            func_str_lst.append(func_str)
        return "\n".join(func_str_lst)

    def build_add(self) -> str:
        if self.node_config.add_function_name is None:
            return ""
        return f"""
@classmethod
async def add(cls, *, input: Add{self.node_name}Input, resolver: {self.resolver_name} = None, upsert: bool = False) -> {self.node_name}:
    return await cls._add(input=input, given_resolver=resolver, upsert=upsert)
        """

    def build_update(self) -> str:
        if self.node_config.update_function_name is None:
            return ""
        arg_str_lst: T.List[str] = []
        to_set_names: T.List[str] = []
        to_remove_names: T.List[str] = []
        for func in self.edge_functions:
            if func.name.endswith("Aggregate"):
                continue
            main_str = ""
            python_type_and_value = (
                f"{func.return_type_python(remove_optional_set=True)} = None"
            )
            set_str = f"{func.name}: {python_type_and_value}"
            to_set_names.append(func.name)
            main_str += set_str
            if not func.is_required_for_node():
                remove_str = f"remove_{func.name}: {python_type_and_value}"
                main_str += f", {remove_str}"
                to_remove_names.append(func.name)
            arg_str_lst.append(main_str)
        edges_arg_str = ", ".join(arg_str_lst)
        to_set_d_lst: T.List[str] = [f'"{name}": {name}' for name in to_set_names]
        to_remove_d_lst: T.List[str] = [
            f'"{name}": remove_{name}' for name in to_remove_names
        ]
        to_set_d_str = f'{{{", ".join(to_set_d_lst)}}}'
        to_remove_d_str = f'{{{", ".join(to_remove_d_lst)}}}'
        return f"""
async def update(self, resolver: {self.resolver_name} = None, {edges_arg_str}) -> bool:
    return await self._update(given_resolver=resolver, to_set={to_set_d_str}, to_remove={to_remove_d_str})
        """

    @property
    def add_model_name(self) -> str:
        return f"Add{self.node_name}Input"

    @property
    def patch_model_name(self) -> str:
        return f"{self.node_name}Patch"

    @property
    def ref_model_name(self) -> str:
        return f"{self.node_name}Ref"

    @staticmethod
    def node_name_from_node_str(node_str: str) -> str:
        pattern = "type (\w*) {"
        return re.findall(pattern, node_str)[0]

    def build_resolver(self) -> str:
        resolver_builder = ResolverBuilder(node_builder=self)
        get_params = resolver_builder.build_get_params()
        query_params = resolver_builder.build_query_params()
        edges = resolver_builder.build_edges()

        classes_str_lst = [get_params, query_params, edges]
        classes_str = "\n\n".join(classes_str_lst)
        classes_str = format_str(classes_str, mode=FileMode())

        get_functions = resolver_builder.build_get_functions()
        query_functions = resolver_builder.build_query_functions()
        edge_functions = resolver_builder.build_edge_functions()

        functions_str_lst = [get_functions, query_functions, edge_functions]
        functions_str = "\n\n".join(functions_str_lst)
        functions_str = format_str(functions_str, mode=FileMode())

        edges_str = f"{self.node_name}Edges"
        query_str = f"{self.node_name}QueryParams"

        resolver_header = f"""
class {self.node_name}Resolver(Resolver[{self.node_name}]):
    node: ClassVar[Type[{self.node_name}]] = {self.node_name}
    edges: {edges_str} = Field(default_factory={edges_str})
    query_params: {query_str} = Field(default_factory={query_str}) 
        """

        classes_with_resolver_header = f"{classes_str}\n{resolver_header}"
        classes_with_resolver_header = format_str(
            classes_with_resolver_header, mode=FileMode()
        )

        full_s = f"{classes_with_resolver_header}\n{indent_lines(functions_str, indent='    ')}"
        full_s = format_str(full_s, mode=FileMode())
        return full_s

    @staticmethod
    def add_parens_to_node_types(node_str: str, node_names: T.List[str]) -> str:
        for node_name in node_names:
            hidden_types_pattern = rf"[^)](: [/[]*{node_name}[!\]]*\s)"
            matches = re.findall(hidden_types_pattern, node_str)
            for match in matches:
                node_str = node_str.replace(match, match.replace(":", "():"))
        return node_str

    def build_update_forward_ref_for_edges_line(self):
        return f"{self.node_name}Edges.update_forward_refs()"

    def build(self) -> str:
        only_fields_node_str = filter_out_funcs_from_type(self.node_str)
        node_fields: T.List[Arg] = Arg.from_str(only_fields_node_str)
        resolver_builder = ResolverBuilder(node_builder=self)
        get_names = []
        if resolver_builder.get_func:
            get_names = set([arg.name for arg in resolver_builder.get_func.args])
        node_field_str_lst: T.List[str] = []
        for field in node_fields:
            allow_mutation = field.name not in get_names
            node_field_str = field.full_line_for_arg(
                use_field=True,
                allow_mutation=allow_mutation,
                iterable_type=IterableType.SET,
            )
            node_field_str_lst.append(node_field_str)
        node_field_strs = "\n".join(node_field_str_lst)
        resolver_line = (
            f"{self.node_name}.{NODE_CONFIG_NAME}.resolver = {self.resolver_name}"
        )
        header = f"class {self.node_name}(Node):\n{indent_lines(node_field_strs, indent=DEFAULT_INDENT)}"
        lines = [
            header,
            indent_lines(self.build_edge_functions(), indent=DEFAULT_INDENT),
            indent_lines(self.build_add(), indent=DEFAULT_INDENT),
            indent_lines(self.build_update(), indent=DEFAULT_INDENT),
            indent_lines(self.node_config.to_config_class(), indent=DEFAULT_INDENT),
            self.build_resolver(),
            resolver_line,
        ]

        final_s = "\n".join(lines)
        final_s = format_str(final_s, mode=FileMode())
        return final_s


class ParamsType(str, Enum):
    GET = "get"
    QUERY = "query"


def build_params(
    params_type: ParamsType, func: T.Optional[Function], node_name: str
) -> str:
    args_str = (
        "\n\t".join([arg.full_line_for_arg() for arg in func.args]) if func else "pass"
    )
    return f"class {node_name}{params_type.value.capitalize()}Params(Params):\n\t{args_str}"


class ResolverBuilder:
    def __init__(self, node_builder: NodeBuilder):
        self.node_builder = node_builder
        self.query_str = node_builder.query_str
        self.query_functions: T.List[Function] = Function.from_str(self.query_str)
        self.query_functions_d: T.Dict[str, Function] = {
            f.name: f for f in self.query_functions
        }

    @property
    def get_func(self) -> T.Optional[Function]:
        if get_function_name := self.node_builder.node_config.get_function_name:
            return self.query_functions_d[get_function_name]
        return None

    @property
    def query_func(self) -> T.Optional[Function]:
        if query_function_name := self.node_builder.node_config.query_function_name:
            return self.query_functions_d[query_function_name]
        return None

    def build_get_params(self) -> str:
        return build_params(
            params_type=ParamsType.GET,
            func=self.get_func,
            node_name=self.node_builder.node_name,
        )

    def build_query_params(self) -> str:
        return build_params(
            params_type=ParamsType.QUERY,
            func=self.query_func,
            node_name=self.node_builder.node_name,
        )

    def build_edges(self) -> str:
        f_str_lst: T.List[str] = []
        for func in self.node_builder.edge_functions:
            f_str = f"{func.name}: Optional[{func.return_node}Resolver] = None"
            f_str_lst.append(f_str)
        f_str = "\n\t".join(f_str_lst)
        if not f_str.strip():
            f_str = "pass"
        return f"class {self.node_builder.node_name}Edges(BaseModel):\n\t{f_str}"

    def build_get_functions(self) -> str:
        if not self.get_func:
            return ""
        args_str = ", ".join([arg.full_line_for_arg() for arg in self.get_func.args])
        kwargs_d_str_inner = ", ".join(
            f'"{f.name}": {f.name}' for f in self.get_func.args
        )
        kwargs_d_str = f"{{{kwargs_d_str_inner}}}"
        get_str = f"""
async def get(self, {args_str}) -> Optional[{self.node_builder.node_name}]:
    return await self._get({kwargs_d_str})
        """
        # now do gerror
        print_str = " and ".join([f"{{{f.name}=}}" for f in self.get_func.args])
        gerror_str = f"""
async def gerror(self, {args_str}) -> {self.node_builder.node_name}:
    node = await self.get({kwargs_d_str_inner.replace('"', '').replace(':', '=')})
    if not node:
        raise GQLException(f"No {self.node_builder.node_name} with {print_str}")
    return node
        """
        return f"{get_str}\n\n{gerror_str}"

    def build_query_functions(self) -> str:
        if not self.query_func:
            return ""
        f_str_lst: T.List[str] = []
        for arg in self.query_func.args:
            f_str = f"""
def {arg.name}(self, {arg.full_line_for_arg()}, /) -> {self.node_builder.resolver_name}:
    self.query_params.{arg.name} = {arg.name}
    return self
                    """
            f_str_lst.append(f_str.strip())
        return "\n\n".join(f_str_lst)

    def build_edge_functions(self) -> str:
        f_str_lst: T.List[str] = []
        for func in self.node_builder.edge_functions:
            return_resolver = f"{func.return_node}Resolver"
            f_str = f"""
def {func.name}(self, _: Optional[{return_resolver}] = None, /) -> {self.node_builder.resolver_name}:
    self.edges.{func.name} = _ or {return_resolver}()
    return self
            """
            f_str_lst.append(f_str.strip())
        return "\n\n".join(f_str_lst)


def get_node_str(main_str: str, node_name: str) -> str:
    pattern = rf"type {node_name} {{[\s\w:!\[\]\(\),]*}}"
    matches = re.findall(pattern, main_str)
    if len(matches) != 1:
        raise Exception(f"Matches not right: {matches=}")
    return matches[0]


def build_nodes(gql_schema_str: str, node_configs: T.List[NodeConfig]) -> str:
    # find all node chunks then create builder from them and GO
    query_str = get_node_str(main_str=gql_schema_str, node_name="Query")
    node_str_lst: T.List[str] = []
    for node_config in node_configs:
        node_str = get_node_str(
            main_str=gql_schema_str, node_name=node_config.node_name
        )
        node_str_lst.append(
            NodeBuilder(
                node_str=node_str,
                node_config=node_config,
                query_str=query_str,
                all_node_configs=node_configs,
            ).build()
        )
    return "\n\n".join(node_str_lst)


def build_enums(gql_schema_str: str) -> str:
    pattern = r"enum [\w]* {[\s\w]*}"
    enum_chunks = re.findall(pattern, gql_schema_str)
    python_enums_strs: T.List[str] = []
    for enum_chunk in enum_chunks:
        name, values = re.findall(r"enum (\w*) {([\w\s]*)}", enum_chunk)[0]
        values_str = "\n".join(
            [f'{v.strip()} = "{v.strip()}"' for v in values.split("\n") if v]
        )
        enum_str = (
            f"class {name}(str, Enum):\n{indent_lines(values_str, indent='    ')}"
        )
        python_enums_strs.append(enum_str)
    return "\n".join(python_enums_strs)


def build_inputs(gql_schema_str: str) -> str:
    pattern = r"input (\w*) {([\w\s:\[!\]]*)}"
    input_chunks = re.findall(pattern, gql_schema_str)
    python_model_strs: T.List[str] = []
    for input_chunk in input_chunks:
        name, fields = input_chunk
        fields: T.List[Arg] = Arg.from_str(fields)
        field_str_lst = [field.full_line_for_arg(use_field=True) for field in fields]
        input_fields_str = "\n".join(field_str_lst)
        input_str = f"class {name}({ORM_MODEL_NAME}):\n{indent_lines(s=input_fields_str, indent=DEFAULT_INDENT)}"
        python_model_strs.append(input_str)
    return "\n".join(python_model_strs)


def filter_out_funcs_from_type(type_str: str) -> str:
    all_of_function_pattern = r"\w*\([\w*:\s,]*\): [\w!\]\[]*"
    s = re.sub(all_of_function_pattern, "", type_str).strip()
    return s


def build_types(gql_schema_str: str, node_names: T.List[str]) -> str:
    node_names = [*node_names, "Query", "Mutation"]
    pattern = r"type (\w*) {([\w\s:\[!\]\(\),]*)}"
    input_chunks = re.findall(pattern, gql_schema_str)
    python_model_strs: T.List[str] = []
    for input_chunk in input_chunks:
        # now remove function code
        name, _ = input_chunk
        if name in node_names:
            continue
        filtered_chunk = filter_out_funcs_from_type(_)
        fields: T.List[Arg] = Arg.from_str(filtered_chunk)
        field_str_lst = [field.full_line_for_arg(use_field=True) for field in fields]
        input_fields_str = "\n".join(field_str_lst)
        input_str = f"class {name}({ORM_MODEL_NAME}):\n{indent_lines(s=input_fields_str, indent=DEFAULT_INDENT)}"
        python_model_strs.append(input_str)
    s = "\n".join(python_model_strs)
    # print(s)
    return s


student_type_str = """
type Student {
  id: ID!
  username: String!
  name: String!
  age: Int!
  taught_by(filter: TeacherFilter): Teacher!
  is_friends_with(
    filter: StudentFilter
    order: StudentOrder
    first: Int
    offset: Int
  ): [Student!]
  optional_field: String
  optional_list: [String!]
  created_at: DateTime
  favorite_artist_id: String!
  favorite_artist: BeatGigArtist
  is_friends_withAggregate(filter: StudentFilter): StudentAggregateResult
}
"""


query_type_str = """
type Query {
  getArtistBeatGig(slug: String!): BeatGigArtist
  add(a: Int, b: Int): Int!
  getUser(id: String, slug: String): User
  queryUser(
    filter: UserFilter
    order: UserOrder
    first: Int
    offset: Int
  ): [User]
  aggregateUser(filter: UserFilter): UserAggregateResult
  getArtist(id: String, slug: String): Artist
  queryArtist(
    filter: ArtistFilter
    order: ArtistOrder
    first: Int
    offset: Int
  ): [Artist]
  aggregateArtist(filter: ArtistFilter): ArtistAggregateResult
  getVenue(id: String, slug: String): Venue
  queryVenue(
    filter: VenueFilter
    order: VenueOrder
    first: Int
    offset: Int
  ): [Venue]
  aggregateVenue(filter: VenueFilter): VenueAggregateResult
  getBooking(id: String!): Booking
  queryBooking(
    filter: BookingFilter
    order: BookingOrder
    first: Int
    offset: Int
  ): [Booking]
  aggregateBooking(filter: BookingFilter): BookingAggregateResult
  getTeacher(id: ID, username: String): Teacher
  queryTeacher(
    filter: TeacherFilter
    order: TeacherOrder
    first: Int
    offset: Int
  ): [Teacher]
  aggregateTeacher(filter: TeacherFilter): TeacherAggregateResult
  getStudent(id: ID, username: String): Student
  queryStudent(
    filter: StudentFilter
    order: StudentOrder
    first: Int
    offset: Int
  ): [Student]
  aggregateStudent(filter: StudentFilter): StudentAggregateResult
}
"""


def function_test():
    funcs = Function.from_str(student_type_str)
    # print(funcs)
    assert funcs[0].name == "taught_by"
    assert funcs[0].args[0].name == "filter"
    assert funcs[0].args[0].type == "TeacherFilter"
    assert funcs[0].return_type == "Teacher!"
    assert funcs[0].return_node == "Teacher"
    assert funcs[0].args[0].python_type() == "Optional[TeacherFilter]"
    assert funcs[0].args[0].value(use_field=False) == "None"
    assert funcs[0].args[0].value(use_field=True) == "Field(None, allow_mutation=True)"
    assert (
        funcs[0].args[0].value(use_field=True, allow_mutation=False)
        == "Field(None, allow_mutation=False)"
    )

    assert funcs[1].name == "is_friends_with"
    assert funcs[1].args[2].python_type() == "Optional[int]"
    assert funcs[1].args[2].value(use_field=False) == "None"


from pathlib import Path


def get_class_names_from_str(s: str) -> T.List[str]:
    class_names_pattern = r"class (\w*)\("
    return re.findall(class_names_pattern, s)


def build_orm(path: Path, node_configs: T.List[NodeConfig]) -> None:
    node_names = [c.node_name for c in node_configs]
    gql_schema_str = open("dgraph_original.graphql", "r").read()
    enums = build_enums(gql_schema_str=gql_schema_str)
    inputs = build_inputs(gql_schema_str=gql_schema_str)
    types = build_types(gql_schema_str=gql_schema_str, node_names=node_names)
    nodes_str = build_nodes(gql_schema_str=gql_schema_str, node_configs=node_configs)
    update_forward_ref_lines = [
        f"{n.node_name}Edges.update_forward_refs()" for n in node_configs
    ]
    update_forward_ref_nodes = [
        f"{n.node_name}.update_forward_refs()" for n in node_configs
    ]

    update_forward_ref_lines_str = "\n".join(update_forward_ref_lines)
    update_forward_ref_nodes_str = "\n".join(update_forward_ref_nodes)

    input_names = get_class_names_from_str(inputs)
    type_names = get_class_names_from_str(types)
    update_forward_ref_input_str = "\n".join(
        [f"{name}.update_forward_refs()" for name in input_names]
    )
    update_forward_ref_type_str = "\n".join(
        [f"{name}.update_forward_refs()" for name in type_names]
    )

    final_s = f"{imports()}\n\n{enums}\n\n{inputs}\n\n{types}\n\n{nodes_str}\n\n{update_forward_ref_input_str}\n\n{update_forward_ref_type_str}\n\n{update_forward_ref_lines_str}\n\n{update_forward_ref_nodes_str}"
    s = format_str(final_s, mode=FileMode())
    open(path, "w").write(s)


def node_configs_from_json(json_path: Path) -> T.List[NodeConfig]:
    config = json.loads(open(json_path, "r").read())
    node_configs: T.List[NodeConfig] = []
    for url in config:
        nodes = config[url]["nodes"]
        for node_name, data in nodes.items():
            if data.get("default", False):
                node_config = NodeConfig.default_from_node_name(node_name, url=url)
            else:
                config_data = data.get("config", {})
                node_config = NodeConfig(node_name=node_name, url=url, **config_data)
            node_configs.append(node_config)
            if data.get("aggregate", False):
                node_configs.append(node_config.create_aggregate())
    return node_configs


def go():
    node_configs = node_configs_from_json(Path("gql_config.json"))
    path = Path("node_testing.py")
    build_orm(path=path, node_configs=node_configs)
    print(f"{path=}")


if __name__ == "__main__":
    function_test()
    go()
