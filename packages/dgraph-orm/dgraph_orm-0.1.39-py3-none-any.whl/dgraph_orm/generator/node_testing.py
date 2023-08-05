from __future__ import annotations
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field
from dgraph_orm import GQLInput, Node, GQLException
from dgraph_orm.resolver import Params, Resolver
from typing import Optional, Set, Type, ClassVar, List


class ArtistHasFilter(str, Enum):
    id = "id"
    slug = "slug"
    name = "name"
    sellers = "sellers"
    bookings = "bookings"


class ArtistOrderable(str, Enum):
    id = "id"
    slug = "slug"
    name = "name"


class BookingHasFilter(str, Enum):
    id = "id"
    artist = "artist"
    venue = "venue"
    created_at = "created_at"
    created_by = "created_by"
    status = "status"


class BookingOrderable(str, Enum):
    id = "id"
    created_at = "created_at"
    status = "status"


class DgraphIndex(str, Enum):
    int = "int"
    int64 = "int64"
    float = "float"
    bool = "bool"
    hash = "hash"
    exact = "exact"
    term = "term"
    fulltext = "fulltext"
    trigram = "trigram"
    regexp = "regexp"
    year = "year"
    month = "month"
    day = "day"
    hour = "hour"
    geo = "geo"


class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class Mode(str, Enum):
    BATCH = "BATCH"
    SINGLE = "SINGLE"


class StudentHasFilter(str, Enum):
    username = "username"
    name = "name"
    age = "age"
    taught_by = "taught_by"
    is_friends_with = "is_friends_with"
    optional_field = "optional_field"
    optional_list = "optional_list"
    created_at = "created_at"
    favorite_artist_id = "favorite_artist_id"


class StudentOrderable(str, Enum):
    username = "username"
    name = "name"
    age = "age"
    optional_field = "optional_field"
    created_at = "created_at"
    favorite_artist_id = "favorite_artist_id"


class TeacherHasFilter(str, Enum):
    username = "username"
    name = "name"
    teaches = "teaches"


class TeacherOrderable(str, Enum):
    username = "username"
    name = "name"


class UserHasFilter(str, Enum):
    id = "id"
    slug = "slug"
    name = "name"
    artists = "artists"
    venues = "venues"
    created_bookings = "created_bookings"


class UserOrderable(str, Enum):
    id = "id"
    slug = "slug"
    name = "name"


class VenueHasFilter(str, Enum):
    id = "id"
    slug = "slug"
    name = "name"
    owners = "owners"
    bookings = "bookings"


class VenueOrderable(str, Enum):
    id = "id"
    slug = "slug"
    name = "name"


class AddArtistInput(GQLInput):
    id: str = Field(..., allow_mutation=True)
    slug: str = Field(..., allow_mutation=True)
    name: str = Field(..., allow_mutation=True)
    sellers: Optional[List[Optional[UserRef]]] = Field(None, allow_mutation=True)
    bookings: Optional[List[Optional[BookingRef]]] = Field(None, allow_mutation=True)


class AddBookingInput(GQLInput):
    id: str = Field(..., allow_mutation=True)
    artist: ArtistRef = Field(..., allow_mutation=True)
    venue: VenueRef = Field(..., allow_mutation=True)
    created_at: datetime = Field(..., allow_mutation=True)
    created_by: Optional[UserRef] = Field(None, allow_mutation=True)
    status: str = Field(..., allow_mutation=True)


class AddStudentInput(GQLInput):
    username: str = Field(..., allow_mutation=True)
    name: str = Field(..., allow_mutation=True)
    age: int = Field(..., allow_mutation=True)
    taught_by: TeacherRef = Field(..., allow_mutation=True)
    is_friends_with: Optional[List[StudentRef]] = Field(None, allow_mutation=True)
    optional_field: Optional[str] = Field(None, allow_mutation=True)
    optional_list: Optional[List[str]] = Field(None, allow_mutation=True)
    created_at: Optional[datetime] = Field(None, allow_mutation=True)
    favorite_artist_id: str = Field(..., allow_mutation=True)


class AddTeacherInput(GQLInput):
    username: str = Field(..., allow_mutation=True)
    name: str = Field(..., allow_mutation=True)
    teaches: Optional[List[StudentRef]] = Field(None, allow_mutation=True)


class AddUserInput(GQLInput):
    id: str = Field(..., allow_mutation=True)
    slug: str = Field(..., allow_mutation=True)
    name: str = Field(..., allow_mutation=True)
    artists: Optional[List[Optional[ArtistRef]]] = Field(None, allow_mutation=True)
    venues: Optional[List[Optional[VenueRef]]] = Field(None, allow_mutation=True)
    created_bookings: Optional[List[Optional[BookingRef]]] = Field(
        None, allow_mutation=True
    )


class AddVenueInput(GQLInput):
    id: str = Field(..., allow_mutation=True)
    slug: str = Field(..., allow_mutation=True)
    name: str = Field(..., allow_mutation=True)
    owners: Optional[List[Optional[UserRef]]] = Field(None, allow_mutation=True)
    bookings: Optional[List[Optional[BookingRef]]] = Field(None, allow_mutation=True)


class ArtistFilter(GQLInput):
    id: Optional[StringHashFilter] = Field(None, allow_mutation=True)
    slug: Optional[StringHashFilter] = Field(None, allow_mutation=True)
    name: Optional[StringFullTextFilter_StringRegExpFilter_StringTermFilter] = Field(
        None, allow_mutation=True
    )
    has: Optional[List[Optional[ArtistHasFilter]]] = Field(None, allow_mutation=True)
    and_: Optional[List[Optional[ArtistFilter]]] = Field(
        None, allow_mutation=True, alias="and"
    )
    or_: Optional[List[Optional[ArtistFilter]]] = Field(
        None, allow_mutation=True, alias="or"
    )
    not_: Optional[ArtistFilter] = Field(None, allow_mutation=True, alias="not")


class ArtistOrder(GQLInput):
    asc: Optional[ArtistOrderable] = Field(None, allow_mutation=True)
    desc: Optional[ArtistOrderable] = Field(None, allow_mutation=True)
    then: Optional[ArtistOrder] = Field(None, allow_mutation=True)


class ArtistPatch(GQLInput):
    name: Optional[str] = Field(None, allow_mutation=True)
    sellers: Optional[List[Optional[UserRef]]] = Field(None, allow_mutation=True)
    bookings: Optional[List[Optional[BookingRef]]] = Field(None, allow_mutation=True)


class ArtistRef(GQLInput):
    id: Optional[str] = Field(None, allow_mutation=True)
    slug: Optional[str] = Field(None, allow_mutation=True)
    name: Optional[str] = Field(None, allow_mutation=True)
    sellers: Optional[List[Optional[UserRef]]] = Field(None, allow_mutation=True)
    bookings: Optional[List[Optional[BookingRef]]] = Field(None, allow_mutation=True)


class AuthRule(GQLInput):
    and_: Optional[List[Optional[AuthRule]]] = Field(
        None, allow_mutation=True, alias="and"
    )
    or_: Optional[List[Optional[AuthRule]]] = Field(
        None, allow_mutation=True, alias="or"
    )
    not_: Optional[AuthRule] = Field(None, allow_mutation=True, alias="not")
    rule: Optional[str] = Field(None, allow_mutation=True)


class BookingFilter(GQLInput):
    id: Optional[StringHashFilter] = Field(None, allow_mutation=True)
    has: Optional[List[Optional[BookingHasFilter]]] = Field(None, allow_mutation=True)
    and_: Optional[List[Optional[BookingFilter]]] = Field(
        None, allow_mutation=True, alias="and"
    )
    or_: Optional[List[Optional[BookingFilter]]] = Field(
        None, allow_mutation=True, alias="or"
    )
    not_: Optional[BookingFilter] = Field(None, allow_mutation=True, alias="not")


class BookingOrder(GQLInput):
    asc: Optional[BookingOrderable] = Field(None, allow_mutation=True)
    desc: Optional[BookingOrderable] = Field(None, allow_mutation=True)
    then: Optional[BookingOrder] = Field(None, allow_mutation=True)


class BookingPatch(GQLInput):
    artist: Optional[ArtistRef] = Field(None, allow_mutation=True)
    venue: Optional[VenueRef] = Field(None, allow_mutation=True)
    created_at: Optional[datetime] = Field(None, allow_mutation=True)
    created_by: Optional[UserRef] = Field(None, allow_mutation=True)
    status: Optional[str] = Field(None, allow_mutation=True)


class BookingRef(GQLInput):
    id: Optional[str] = Field(None, allow_mutation=True)
    artist: Optional[ArtistRef] = Field(None, allow_mutation=True)
    venue: Optional[VenueRef] = Field(None, allow_mutation=True)
    created_at: Optional[datetime] = Field(None, allow_mutation=True)
    created_by: Optional[UserRef] = Field(None, allow_mutation=True)
    status: Optional[str] = Field(None, allow_mutation=True)


class ContainsFilter(GQLInput):
    point: Optional[PointRef] = Field(None, allow_mutation=True)
    polygon: Optional[PolygonRef] = Field(None, allow_mutation=True)


class CustomHTTP(GQLInput):
    url: str = Field(..., allow_mutation=True)
    method: HTTPMethod = Field(..., allow_mutation=True)
    body: Optional[str] = Field(None, allow_mutation=True)
    graphql: Optional[str] = Field(None, allow_mutation=True)
    mode: Optional[Mode] = Field(None, allow_mutation=True)
    forwardHeaders: Optional[List[str]] = Field(None, allow_mutation=True)
    secretHeaders: Optional[List[str]] = Field(None, allow_mutation=True)
    introspectionHeaders: Optional[List[str]] = Field(None, allow_mutation=True)
    skipIntrospection: Optional[bool] = Field(None, allow_mutation=True)


class DateTimeFilter(GQLInput):
    eq: Optional[datetime] = Field(None, allow_mutation=True)
    in_: Optional[List[Optional[datetime]]] = Field(
        None, allow_mutation=True, alias="in"
    )
    le: Optional[datetime] = Field(None, allow_mutation=True)
    lt: Optional[datetime] = Field(None, allow_mutation=True)
    ge: Optional[datetime] = Field(None, allow_mutation=True)
    gt: Optional[datetime] = Field(None, allow_mutation=True)
    between: Optional[DateTimeRange] = Field(None, allow_mutation=True)


class DateTimeRange(GQLInput):
    min: datetime = Field(..., allow_mutation=True)
    max: datetime = Field(..., allow_mutation=True)


class FloatFilter(GQLInput):
    eq: Optional[float] = Field(None, allow_mutation=True)
    in_: Optional[List[Optional[float]]] = Field(None, allow_mutation=True, alias="in")
    le: Optional[float] = Field(None, allow_mutation=True)
    lt: Optional[float] = Field(None, allow_mutation=True)
    ge: Optional[float] = Field(None, allow_mutation=True)
    gt: Optional[float] = Field(None, allow_mutation=True)
    between: Optional[FloatRange] = Field(None, allow_mutation=True)


class FloatRange(GQLInput):
    min: float = Field(..., allow_mutation=True)
    max: float = Field(..., allow_mutation=True)


class GenerateMutationParams(GQLInput):
    add: Optional[bool] = Field(None, allow_mutation=True)
    update: Optional[bool] = Field(None, allow_mutation=True)
    delete: Optional[bool] = Field(None, allow_mutation=True)


class GenerateQueryParams(GQLInput):
    get: Optional[bool] = Field(None, allow_mutation=True)
    query: Optional[bool] = Field(None, allow_mutation=True)
    password: Optional[bool] = Field(None, allow_mutation=True)
    aggregate: Optional[bool] = Field(None, allow_mutation=True)


class Int64Filter(GQLInput):
    eq: Optional[int] = Field(None, allow_mutation=True)
    in_: Optional[List[Optional[int]]] = Field(None, allow_mutation=True, alias="in")
    le: Optional[int] = Field(None, allow_mutation=True)
    lt: Optional[int] = Field(None, allow_mutation=True)
    ge: Optional[int] = Field(None, allow_mutation=True)
    gt: Optional[int] = Field(None, allow_mutation=True)
    between: Optional[Int64Range] = Field(None, allow_mutation=True)


class Int64Range(GQLInput):
    min: int = Field(..., allow_mutation=True)
    max: int = Field(..., allow_mutation=True)


class IntersectsFilter(GQLInput):
    polygon: Optional[PolygonRef] = Field(None, allow_mutation=True)
    multiPolygon: Optional[MultiPolygonRef] = Field(None, allow_mutation=True)


class IntFilter(GQLInput):
    eq: Optional[int] = Field(None, allow_mutation=True)
    in_: Optional[List[Optional[int]]] = Field(None, allow_mutation=True, alias="in")
    le: Optional[int] = Field(None, allow_mutation=True)
    lt: Optional[int] = Field(None, allow_mutation=True)
    ge: Optional[int] = Field(None, allow_mutation=True)
    gt: Optional[int] = Field(None, allow_mutation=True)
    between: Optional[IntRange] = Field(None, allow_mutation=True)


class IntRange(GQLInput):
    min: int = Field(..., allow_mutation=True)
    max: int = Field(..., allow_mutation=True)


class MultiPolygonRef(GQLInput):
    polygons: List[PolygonRef] = Field(..., allow_mutation=True)


class NearFilter(GQLInput):
    distance: float = Field(..., allow_mutation=True)
    coordinate: PointRef = Field(..., allow_mutation=True)


class PointGeoFilter(GQLInput):
    near: Optional[NearFilter] = Field(None, allow_mutation=True)
    within: Optional[WithinFilter] = Field(None, allow_mutation=True)


class PointListRef(GQLInput):
    points: List[PointRef] = Field(..., allow_mutation=True)


class PointRef(GQLInput):
    longitude: float = Field(..., allow_mutation=True)
    latitude: float = Field(..., allow_mutation=True)


class PolygonGeoFilter(GQLInput):
    near: Optional[NearFilter] = Field(None, allow_mutation=True)
    within: Optional[WithinFilter] = Field(None, allow_mutation=True)
    contains: Optional[ContainsFilter] = Field(None, allow_mutation=True)
    intersects: Optional[IntersectsFilter] = Field(None, allow_mutation=True)


class PolygonRef(GQLInput):
    coordinates: List[PointListRef] = Field(..., allow_mutation=True)


class StringExactFilter(GQLInput):
    eq: Optional[str] = Field(None, allow_mutation=True)
    in_: Optional[List[Optional[str]]] = Field(None, allow_mutation=True, alias="in")
    le: Optional[str] = Field(None, allow_mutation=True)
    lt: Optional[str] = Field(None, allow_mutation=True)
    ge: Optional[str] = Field(None, allow_mutation=True)
    gt: Optional[str] = Field(None, allow_mutation=True)
    between: Optional[StringRange] = Field(None, allow_mutation=True)


class StringFullTextFilter(GQLInput):
    alloftext: Optional[str] = Field(None, allow_mutation=True)
    anyoftext: Optional[str] = Field(None, allow_mutation=True)


class StringFullTextFilter_StringRegExpFilter_StringTermFilter(GQLInput):
    alloftext: Optional[str] = Field(None, allow_mutation=True)
    anyoftext: Optional[str] = Field(None, allow_mutation=True)
    regexp: Optional[str] = Field(None, allow_mutation=True)
    allofterms: Optional[str] = Field(None, allow_mutation=True)
    anyofterms: Optional[str] = Field(None, allow_mutation=True)


class StringHashFilter(GQLInput):
    eq: Optional[str] = Field(None, allow_mutation=True)
    in_: Optional[List[Optional[str]]] = Field(None, allow_mutation=True, alias="in")


class StringRange(GQLInput):
    min: str = Field(..., allow_mutation=True)
    max: str = Field(..., allow_mutation=True)


class StringRegExpFilter(GQLInput):
    regexp: Optional[str] = Field(None, allow_mutation=True)


class StringTermFilter(GQLInput):
    allofterms: Optional[str] = Field(None, allow_mutation=True)
    anyofterms: Optional[str] = Field(None, allow_mutation=True)


class StudentFilter(GQLInput):
    id: Optional[List[str]] = Field(None, allow_mutation=True)
    username: Optional[StringHashFilter] = Field(None, allow_mutation=True)
    has: Optional[List[Optional[StudentHasFilter]]] = Field(None, allow_mutation=True)
    and_: Optional[List[Optional[StudentFilter]]] = Field(
        None, allow_mutation=True, alias="and"
    )
    or_: Optional[List[Optional[StudentFilter]]] = Field(
        None, allow_mutation=True, alias="or"
    )
    not_: Optional[StudentFilter] = Field(None, allow_mutation=True, alias="not")


class StudentOrder(GQLInput):
    asc: Optional[StudentOrderable] = Field(None, allow_mutation=True)
    desc: Optional[StudentOrderable] = Field(None, allow_mutation=True)
    then: Optional[StudentOrder] = Field(None, allow_mutation=True)


class StudentPatch(GQLInput):
    name: Optional[str] = Field(None, allow_mutation=True)
    age: Optional[int] = Field(None, allow_mutation=True)
    taught_by: Optional[TeacherRef] = Field(None, allow_mutation=True)
    is_friends_with: Optional[List[StudentRef]] = Field(None, allow_mutation=True)
    optional_field: Optional[str] = Field(None, allow_mutation=True)
    optional_list: Optional[List[str]] = Field(None, allow_mutation=True)
    created_at: Optional[datetime] = Field(None, allow_mutation=True)
    favorite_artist_id: Optional[str] = Field(None, allow_mutation=True)


class StudentRef(GQLInput):
    id: Optional[str] = Field(None, allow_mutation=True)
    username: Optional[str] = Field(None, allow_mutation=True)
    name: Optional[str] = Field(None, allow_mutation=True)
    age: Optional[int] = Field(None, allow_mutation=True)
    taught_by: Optional[TeacherRef] = Field(None, allow_mutation=True)
    is_friends_with: Optional[List[StudentRef]] = Field(None, allow_mutation=True)
    optional_field: Optional[str] = Field(None, allow_mutation=True)
    optional_list: Optional[List[str]] = Field(None, allow_mutation=True)
    created_at: Optional[datetime] = Field(None, allow_mutation=True)
    favorite_artist_id: Optional[str] = Field(None, allow_mutation=True)


class TeacherFilter(GQLInput):
    id: Optional[List[str]] = Field(None, allow_mutation=True)
    username: Optional[StringHashFilter] = Field(None, allow_mutation=True)
    has: Optional[List[Optional[TeacherHasFilter]]] = Field(None, allow_mutation=True)
    and_: Optional[List[Optional[TeacherFilter]]] = Field(
        None, allow_mutation=True, alias="and"
    )
    or_: Optional[List[Optional[TeacherFilter]]] = Field(
        None, allow_mutation=True, alias="or"
    )
    not_: Optional[TeacherFilter] = Field(None, allow_mutation=True, alias="not")


class TeacherOrder(GQLInput):
    asc: Optional[TeacherOrderable] = Field(None, allow_mutation=True)
    desc: Optional[TeacherOrderable] = Field(None, allow_mutation=True)
    then: Optional[TeacherOrder] = Field(None, allow_mutation=True)


class TeacherPatch(GQLInput):
    name: Optional[str] = Field(None, allow_mutation=True)
    teaches: Optional[List[StudentRef]] = Field(None, allow_mutation=True)


class TeacherRef(GQLInput):
    id: Optional[str] = Field(None, allow_mutation=True)
    username: Optional[str] = Field(None, allow_mutation=True)
    name: Optional[str] = Field(None, allow_mutation=True)
    teaches: Optional[List[StudentRef]] = Field(None, allow_mutation=True)


class UpdateArtistInput(GQLInput):
    filter: ArtistFilter = Field(..., allow_mutation=True)
    set: Optional[ArtistPatch] = Field(None, allow_mutation=True)
    remove: Optional[ArtistPatch] = Field(None, allow_mutation=True)


class UpdateBookingInput(GQLInput):
    filter: BookingFilter = Field(..., allow_mutation=True)
    set: Optional[BookingPatch] = Field(None, allow_mutation=True)
    remove: Optional[BookingPatch] = Field(None, allow_mutation=True)


class UpdateStudentInput(GQLInput):
    filter: StudentFilter = Field(..., allow_mutation=True)
    set: Optional[StudentPatch] = Field(None, allow_mutation=True)
    remove: Optional[StudentPatch] = Field(None, allow_mutation=True)


class UpdateTeacherInput(GQLInput):
    filter: TeacherFilter = Field(..., allow_mutation=True)
    set: Optional[TeacherPatch] = Field(None, allow_mutation=True)
    remove: Optional[TeacherPatch] = Field(None, allow_mutation=True)


class UpdateUserInput(GQLInput):
    filter: UserFilter = Field(..., allow_mutation=True)
    set: Optional[UserPatch] = Field(None, allow_mutation=True)
    remove: Optional[UserPatch] = Field(None, allow_mutation=True)


class UpdateVenueInput(GQLInput):
    filter: VenueFilter = Field(..., allow_mutation=True)
    set: Optional[VenuePatch] = Field(None, allow_mutation=True)
    remove: Optional[VenuePatch] = Field(None, allow_mutation=True)


class UserFilter(GQLInput):
    id: Optional[StringHashFilter] = Field(None, allow_mutation=True)
    slug: Optional[StringHashFilter] = Field(None, allow_mutation=True)
    has: Optional[List[Optional[UserHasFilter]]] = Field(None, allow_mutation=True)
    and_: Optional[List[Optional[UserFilter]]] = Field(
        None, allow_mutation=True, alias="and"
    )
    or_: Optional[List[Optional[UserFilter]]] = Field(
        None, allow_mutation=True, alias="or"
    )
    not_: Optional[UserFilter] = Field(None, allow_mutation=True, alias="not")


class UserOrder(GQLInput):
    asc: Optional[UserOrderable] = Field(None, allow_mutation=True)
    desc: Optional[UserOrderable] = Field(None, allow_mutation=True)
    then: Optional[UserOrder] = Field(None, allow_mutation=True)


class UserPatch(GQLInput):
    name: Optional[str] = Field(None, allow_mutation=True)
    artists: Optional[List[Optional[ArtistRef]]] = Field(None, allow_mutation=True)
    venues: Optional[List[Optional[VenueRef]]] = Field(None, allow_mutation=True)
    created_bookings: Optional[List[Optional[BookingRef]]] = Field(
        None, allow_mutation=True
    )


class UserRef(GQLInput):
    id: Optional[str] = Field(None, allow_mutation=True)
    slug: Optional[str] = Field(None, allow_mutation=True)
    name: Optional[str] = Field(None, allow_mutation=True)
    artists: Optional[List[Optional[ArtistRef]]] = Field(None, allow_mutation=True)
    venues: Optional[List[Optional[VenueRef]]] = Field(None, allow_mutation=True)
    created_bookings: Optional[List[Optional[BookingRef]]] = Field(
        None, allow_mutation=True
    )


class VenueFilter(GQLInput):
    id: Optional[StringHashFilter] = Field(None, allow_mutation=True)
    slug: Optional[StringHashFilter] = Field(None, allow_mutation=True)
    has: Optional[List[Optional[VenueHasFilter]]] = Field(None, allow_mutation=True)
    and_: Optional[List[Optional[VenueFilter]]] = Field(
        None, allow_mutation=True, alias="and"
    )
    or_: Optional[List[Optional[VenueFilter]]] = Field(
        None, allow_mutation=True, alias="or"
    )
    not_: Optional[VenueFilter] = Field(None, allow_mutation=True, alias="not")


class VenueOrder(GQLInput):
    asc: Optional[VenueOrderable] = Field(None, allow_mutation=True)
    desc: Optional[VenueOrderable] = Field(None, allow_mutation=True)
    then: Optional[VenueOrder] = Field(None, allow_mutation=True)


class VenuePatch(GQLInput):
    name: Optional[str] = Field(None, allow_mutation=True)
    owners: Optional[List[Optional[UserRef]]] = Field(None, allow_mutation=True)
    bookings: Optional[List[Optional[BookingRef]]] = Field(None, allow_mutation=True)


class VenueRef(GQLInput):
    id: Optional[str] = Field(None, allow_mutation=True)
    slug: Optional[str] = Field(None, allow_mutation=True)
    name: Optional[str] = Field(None, allow_mutation=True)
    owners: Optional[List[Optional[UserRef]]] = Field(None, allow_mutation=True)
    bookings: Optional[List[Optional[BookingRef]]] = Field(None, allow_mutation=True)


class WithinFilter(GQLInput):
    polygon: PolygonRef = Field(..., allow_mutation=True)


class AddArtistPayload(GQLInput):
    numUids: Optional[int] = Field(None, allow_mutation=True)


class AddBookingPayload(GQLInput):
    numUids: Optional[int] = Field(None, allow_mutation=True)


class AddStudentPayload(GQLInput):
    numUids: Optional[int] = Field(None, allow_mutation=True)


class AddTeacherPayload(GQLInput):
    numUids: Optional[int] = Field(None, allow_mutation=True)


class AddUserPayload(GQLInput):
    numUids: Optional[int] = Field(None, allow_mutation=True)


class AddVenuePayload(GQLInput):
    numUids: Optional[int] = Field(None, allow_mutation=True)


class DeleteArtistPayload(GQLInput):
    msg: Optional[str] = Field(None, allow_mutation=True)
    numUids: Optional[int] = Field(None, allow_mutation=True)


class DeleteBookingPayload(GQLInput):
    msg: Optional[str] = Field(None, allow_mutation=True)
    numUids: Optional[int] = Field(None, allow_mutation=True)


class DeleteStudentPayload(GQLInput):
    msg: Optional[str] = Field(None, allow_mutation=True)
    numUids: Optional[int] = Field(None, allow_mutation=True)


class DeleteTeacherPayload(GQLInput):
    msg: Optional[str] = Field(None, allow_mutation=True)
    numUids: Optional[int] = Field(None, allow_mutation=True)


class DeleteUserPayload(GQLInput):
    msg: Optional[str] = Field(None, allow_mutation=True)
    numUids: Optional[int] = Field(None, allow_mutation=True)


class DeleteVenuePayload(GQLInput):
    msg: Optional[str] = Field(None, allow_mutation=True)
    numUids: Optional[int] = Field(None, allow_mutation=True)


class MultiPolygon(GQLInput):
    polygons: List[Polygon] = Field(..., allow_mutation=True)


class Point(GQLInput):
    longitude: float = Field(..., allow_mutation=True)
    latitude: float = Field(..., allow_mutation=True)


class PointList(GQLInput):
    points: List[Point] = Field(..., allow_mutation=True)


class Polygon(GQLInput):
    coordinates: List[PointList] = Field(..., allow_mutation=True)


class UpdateArtistPayload(GQLInput):
    numUids: Optional[int] = Field(None, allow_mutation=True)


class UpdateBookingPayload(GQLInput):
    numUids: Optional[int] = Field(None, allow_mutation=True)


class UpdateStudentPayload(GQLInput):
    numUids: Optional[int] = Field(None, allow_mutation=True)


class UpdateTeacherPayload(GQLInput):
    numUids: Optional[int] = Field(None, allow_mutation=True)


class UpdateUserPayload(GQLInput):
    numUids: Optional[int] = Field(None, allow_mutation=True)


class UpdateVenuePayload(GQLInput):
    numUids: Optional[int] = Field(None, allow_mutation=True)


class Student(Node):
    id: str = Field(..., allow_mutation=False)
    username: str = Field(..., allow_mutation=False)
    name: str = Field(..., allow_mutation=True)
    age: int = Field(..., allow_mutation=True)
    optional_field: Optional[str] = Field(None, allow_mutation=True)
    optional_list: Optional[Set[str]] = Field(None, allow_mutation=True)
    created_at: Optional[datetime] = Field(None, allow_mutation=True)
    favorite_artist_id: str = Field(..., allow_mutation=True)

    async def taught_by(
        self,
        resolver: TeacherResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> Teacher:
        return await self.resolve(
            name="taught_by", resolver=resolver, refresh=refresh, use_stale=use_stale
        )

    async def is_friends_with(
        self,
        resolver: StudentResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> List[Student]:
        return await self.resolve(
            name="is_friends_with",
            resolver=resolver,
            refresh=refresh,
            use_stale=use_stale,
        )

    async def favorite_artist(
        self,
        resolver: BeatGigArtistResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> Optional[BeatGigArtist]:
        return await self.resolve(
            name="favorite_artist",
            resolver=resolver,
            refresh=refresh,
            use_stale=use_stale,
        )

    async def is_friends_withAggregate(
        self,
        resolver: StudentAggregateResultResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> Optional[StudentAggregateResult]:
        return await self.resolve(
            name="is_friends_withAggregate",
            resolver=resolver,
            refresh=refresh,
            use_stale=use_stale,
        )

    @classmethod
    async def add(
        cls,
        *,
        input: AddStudentInput,
        resolver: StudentResolver = None,
        upsert: bool = False,
    ) -> Student:
        return await cls._add(input=input, given_resolver=resolver, upsert=upsert)

    async def update(
        self,
        resolver: StudentResolver = None,
        taught_by: Teacher = None,
        is_friends_with: List[Student] = None,
        remove_is_friends_with: List[Student] = None,
        favorite_artist: Optional[BeatGigArtist] = None,
        remove_favorite_artist: Optional[BeatGigArtist] = None,
    ) -> bool:
        return await self._update(
            given_resolver=resolver,
            to_set={
                "taught_by": taught_by,
                "is_friends_with": is_friends_with,
                "favorite_artist": favorite_artist,
            },
            to_remove={
                "is_friends_with": remove_is_friends_with,
                "favorite_artist": remove_favorite_artist,
            },
        )

    class GQL:
        typename = "Student"
        payload_node_name = "student"
        resolver: Type[StudentResolver]

        # models
        add_model: Type[AddStudentInput] = AddStudentInput
        patch_model: Type[StudentPatch] = StudentPatch
        ref_model: Type[StudentRef] = StudentRef

        # functions
        get_function_name: str = "getStudent"
        query_function_name: str = "queryStudent"

        add_function_name: str = "addStudent"
        update_function_name: str = "updateStudent"
        delete_function_name: str = "deleteStudent"

        url: str = "https://sparkling-butterfly.us-east-1.aws.cloud.dgraph.io/graphql"
        uid_field_name: str = "id"


class StudentGetParams(Params):
    id: Optional[str] = None
    username: Optional[str] = None


class StudentQueryParams(Params):
    filter: Optional[StudentFilter] = None
    order: Optional[StudentOrder] = None
    first: Optional[int] = None
    offset: Optional[int] = None


class StudentEdges(BaseModel):
    taught_by: Optional[TeacherResolver] = None
    is_friends_with: Optional[StudentResolver] = None
    favorite_artist: Optional[BeatGigArtistResolver] = None
    is_friends_withAggregate: Optional[StudentAggregateResultResolver] = None


class StudentResolver(Resolver[Student]):
    node: ClassVar[Type[Student]] = Student
    edges: StudentEdges = Field(default_factory=StudentEdges)
    query_params: StudentQueryParams = Field(default_factory=StudentQueryParams)

    async def get(
        self, id: Optional[str] = None, username: Optional[str] = None
    ) -> Optional[Student]:
        return await self._get({"id": id, "username": username})

    async def gerror(
        self, id: Optional[str] = None, username: Optional[str] = None
    ) -> Student:
        node = await self.get(id=id, username=username)
        if not node:
            raise GQLException(f"No Student with {id=} and {username=}")
        return node

    def filter(self, filter: Optional[StudentFilter] = None, /) -> StudentResolver:
        self.query_params.filter = filter
        return self

    def order(self, order: Optional[StudentOrder] = None, /) -> StudentResolver:
        self.query_params.order = order
        return self

    def first(self, first: Optional[int] = None, /) -> StudentResolver:
        self.query_params.first = first
        return self

    def offset(self, offset: Optional[int] = None, /) -> StudentResolver:
        self.query_params.offset = offset
        return self

    def taught_by(self, _: Optional[TeacherResolver] = None, /) -> StudentResolver:
        self.edges.taught_by = _ or TeacherResolver()
        return self

    def is_friends_with(
        self, _: Optional[StudentResolver] = None, /
    ) -> StudentResolver:
        self.edges.is_friends_with = _ or StudentResolver()
        return self

    def favorite_artist(
        self, _: Optional[BeatGigArtistResolver] = None, /
    ) -> StudentResolver:
        self.edges.favorite_artist = _ or BeatGigArtistResolver()
        return self

    def is_friends_withAggregate(
        self, _: Optional[StudentAggregateResultResolver] = None, /
    ) -> StudentResolver:
        self.edges.is_friends_withAggregate = _ or StudentAggregateResultResolver()
        return self


Student.GQL.resolver = StudentResolver


class StudentAggregateResult(Node):
    count: Optional[int] = Field(None, allow_mutation=True)
    usernameMin: Optional[str] = Field(None, allow_mutation=True)
    usernameMax: Optional[str] = Field(None, allow_mutation=True)
    nameMin: Optional[str] = Field(None, allow_mutation=True)
    nameMax: Optional[str] = Field(None, allow_mutation=True)
    ageMin: Optional[int] = Field(None, allow_mutation=True)
    ageMax: Optional[int] = Field(None, allow_mutation=True)
    ageSum: Optional[int] = Field(None, allow_mutation=True)
    ageAvg: Optional[float] = Field(None, allow_mutation=True)
    optional_fieldMin: Optional[str] = Field(None, allow_mutation=True)
    optional_fieldMax: Optional[str] = Field(None, allow_mutation=True)
    created_atMin: Optional[datetime] = Field(None, allow_mutation=True)
    created_atMax: Optional[datetime] = Field(None, allow_mutation=True)
    favorite_artist_idMin: Optional[str] = Field(None, allow_mutation=True)
    favorite_artist_idMax: Optional[str] = Field(None, allow_mutation=True)

    class GQL:
        typename = "StudentAggregateResult"
        payload_node_name = None
        resolver: Type[None]

        # models
        add_model: Type[None] = None
        patch_model: Type[None] = None
        ref_model: Type[None] = None

        # functions
        get_function_name: str = "aggregateStudent"
        query_function_name: str = None

        add_function_name: str = None
        update_function_name: str = None
        delete_function_name: str = None

        url: str = "https://sparkling-butterfly.us-east-1.aws.cloud.dgraph.io/graphql"
        uid_field_name: str = "count"


class StudentAggregateResultGetParams(Params):
    filter: Optional[StudentFilter] = None


class StudentAggregateResultQueryParams(Params):
    pass


class StudentAggregateResultEdges(BaseModel):
    pass


class StudentAggregateResultResolver(Resolver[StudentAggregateResult]):
    node: ClassVar[Type[StudentAggregateResult]] = StudentAggregateResult
    edges: StudentAggregateResultEdges = Field(
        default_factory=StudentAggregateResultEdges
    )
    query_params: StudentAggregateResultQueryParams = Field(
        default_factory=StudentAggregateResultQueryParams
    )

    async def get(
        self, filter: Optional[StudentFilter] = None
    ) -> Optional[StudentAggregateResult]:
        return await self._get({"filter": filter})

    async def gerror(
        self, filter: Optional[StudentFilter] = None
    ) -> StudentAggregateResult:
        node = await self.get(filter=filter)
        if not node:
            raise GQLException(f"No StudentAggregateResult with {filter=}")
        return node


StudentAggregateResult.GQL.resolver = StudentAggregateResultResolver


class Teacher(Node):
    id: str = Field(..., allow_mutation=False)
    username: str = Field(..., allow_mutation=False)
    name: str = Field(..., allow_mutation=True)

    async def teaches(
        self,
        resolver: StudentResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> List[Student]:
        return await self.resolve(
            name="teaches", resolver=resolver, refresh=refresh, use_stale=use_stale
        )

    async def teachesAggregate(
        self,
        resolver: StudentAggregateResultResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> Optional[StudentAggregateResult]:
        return await self.resolve(
            name="teachesAggregate",
            resolver=resolver,
            refresh=refresh,
            use_stale=use_stale,
        )

    @classmethod
    async def add(
        cls,
        *,
        input: AddTeacherInput,
        resolver: TeacherResolver = None,
        upsert: bool = False,
    ) -> Teacher:
        return await cls._add(input=input, given_resolver=resolver, upsert=upsert)

    async def update(
        self,
        resolver: TeacherResolver = None,
        teaches: List[Student] = None,
        remove_teaches: List[Student] = None,
    ) -> bool:
        return await self._update(
            given_resolver=resolver,
            to_set={"teaches": teaches},
            to_remove={"teaches": remove_teaches},
        )

    class GQL:
        typename = "Teacher"
        payload_node_name = "teacher"
        resolver: Type[TeacherResolver]

        # models
        add_model: Type[AddTeacherInput] = AddTeacherInput
        patch_model: Type[TeacherPatch] = TeacherPatch
        ref_model: Type[TeacherRef] = TeacherRef

        # functions
        get_function_name: str = "getTeacher"
        query_function_name: str = "queryTeacher"

        add_function_name: str = "addTeacher"
        update_function_name: str = "updateTeacher"
        delete_function_name: str = "deleteTeacher"

        url: str = "https://sparkling-butterfly.us-east-1.aws.cloud.dgraph.io/graphql"
        uid_field_name: str = "id"


class TeacherGetParams(Params):
    id: Optional[str] = None
    username: Optional[str] = None


class TeacherQueryParams(Params):
    filter: Optional[TeacherFilter] = None
    order: Optional[TeacherOrder] = None
    first: Optional[int] = None
    offset: Optional[int] = None


class TeacherEdges(BaseModel):
    teaches: Optional[StudentResolver] = None
    teachesAggregate: Optional[StudentAggregateResultResolver] = None


class TeacherResolver(Resolver[Teacher]):
    node: ClassVar[Type[Teacher]] = Teacher
    edges: TeacherEdges = Field(default_factory=TeacherEdges)
    query_params: TeacherQueryParams = Field(default_factory=TeacherQueryParams)

    async def get(
        self, id: Optional[str] = None, username: Optional[str] = None
    ) -> Optional[Teacher]:
        return await self._get({"id": id, "username": username})

    async def gerror(
        self, id: Optional[str] = None, username: Optional[str] = None
    ) -> Teacher:
        node = await self.get(id=id, username=username)
        if not node:
            raise GQLException(f"No Teacher with {id=} and {username=}")
        return node

    def filter(self, filter: Optional[TeacherFilter] = None, /) -> TeacherResolver:
        self.query_params.filter = filter
        return self

    def order(self, order: Optional[TeacherOrder] = None, /) -> TeacherResolver:
        self.query_params.order = order
        return self

    def first(self, first: Optional[int] = None, /) -> TeacherResolver:
        self.query_params.first = first
        return self

    def offset(self, offset: Optional[int] = None, /) -> TeacherResolver:
        self.query_params.offset = offset
        return self

    def teaches(self, _: Optional[StudentResolver] = None, /) -> TeacherResolver:
        self.edges.teaches = _ or StudentResolver()
        return self

    def teachesAggregate(
        self, _: Optional[StudentAggregateResultResolver] = None, /
    ) -> TeacherResolver:
        self.edges.teachesAggregate = _ or StudentAggregateResultResolver()
        return self


Teacher.GQL.resolver = TeacherResolver


class TeacherAggregateResult(Node):
    count: Optional[int] = Field(None, allow_mutation=True)
    usernameMin: Optional[str] = Field(None, allow_mutation=True)
    usernameMax: Optional[str] = Field(None, allow_mutation=True)
    nameMin: Optional[str] = Field(None, allow_mutation=True)
    nameMax: Optional[str] = Field(None, allow_mutation=True)

    class GQL:
        typename = "TeacherAggregateResult"
        payload_node_name = None
        resolver: Type[None]

        # models
        add_model: Type[None] = None
        patch_model: Type[None] = None
        ref_model: Type[None] = None

        # functions
        get_function_name: str = "aggregateTeacher"
        query_function_name: str = None

        add_function_name: str = None
        update_function_name: str = None
        delete_function_name: str = None

        url: str = "https://sparkling-butterfly.us-east-1.aws.cloud.dgraph.io/graphql"
        uid_field_name: str = "count"


class TeacherAggregateResultGetParams(Params):
    filter: Optional[TeacherFilter] = None


class TeacherAggregateResultQueryParams(Params):
    pass


class TeacherAggregateResultEdges(BaseModel):
    pass


class TeacherAggregateResultResolver(Resolver[TeacherAggregateResult]):
    node: ClassVar[Type[TeacherAggregateResult]] = TeacherAggregateResult
    edges: TeacherAggregateResultEdges = Field(
        default_factory=TeacherAggregateResultEdges
    )
    query_params: TeacherAggregateResultQueryParams = Field(
        default_factory=TeacherAggregateResultQueryParams
    )

    async def get(
        self, filter: Optional[TeacherFilter] = None
    ) -> Optional[TeacherAggregateResult]:
        return await self._get({"filter": filter})

    async def gerror(
        self, filter: Optional[TeacherFilter] = None
    ) -> TeacherAggregateResult:
        node = await self.get(filter=filter)
        if not node:
            raise GQLException(f"No TeacherAggregateResult with {filter=}")
        return node


TeacherAggregateResult.GQL.resolver = TeacherAggregateResultResolver


class User(Node):
    id: str = Field(..., allow_mutation=False)
    slug: str = Field(..., allow_mutation=False)
    name: str = Field(..., allow_mutation=True)

    async def artists(
        self,
        resolver: ArtistResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> List[Optional[Artist]]:
        return await self.resolve(
            name="artists", resolver=resolver, refresh=refresh, use_stale=use_stale
        )

    async def venues(
        self,
        resolver: VenueResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> List[Optional[Venue]]:
        return await self.resolve(
            name="venues", resolver=resolver, refresh=refresh, use_stale=use_stale
        )

    async def created_bookings(
        self,
        resolver: BookingResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> List[Optional[Booking]]:
        return await self.resolve(
            name="created_bookings",
            resolver=resolver,
            refresh=refresh,
            use_stale=use_stale,
        )

    async def artistsAggregate(
        self,
        resolver: ArtistAggregateResultResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> Optional[ArtistAggregateResult]:
        return await self.resolve(
            name="artistsAggregate",
            resolver=resolver,
            refresh=refresh,
            use_stale=use_stale,
        )

    async def venuesAggregate(
        self,
        resolver: VenueAggregateResultResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> Optional[VenueAggregateResult]:
        return await self.resolve(
            name="venuesAggregate",
            resolver=resolver,
            refresh=refresh,
            use_stale=use_stale,
        )

    async def created_bookingsAggregate(
        self,
        resolver: BookingAggregateResultResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> Optional[BookingAggregateResult]:
        return await self.resolve(
            name="created_bookingsAggregate",
            resolver=resolver,
            refresh=refresh,
            use_stale=use_stale,
        )

    @classmethod
    async def add(
        cls, *, input: AddUserInput, resolver: UserResolver = None, upsert: bool = False
    ) -> User:
        return await cls._add(input=input, given_resolver=resolver, upsert=upsert)

    async def update(
        self,
        resolver: UserResolver = None,
        artists: List[Optional[Artist]] = None,
        remove_artists: List[Optional[Artist]] = None,
        venues: List[Optional[Venue]] = None,
        remove_venues: List[Optional[Venue]] = None,
        created_bookings: List[Optional[Booking]] = None,
        remove_created_bookings: List[Optional[Booking]] = None,
    ) -> bool:
        return await self._update(
            given_resolver=resolver,
            to_set={
                "artists": artists,
                "venues": venues,
                "created_bookings": created_bookings,
            },
            to_remove={
                "artists": remove_artists,
                "venues": remove_venues,
                "created_bookings": remove_created_bookings,
            },
        )

    class GQL:
        typename = "User"
        payload_node_name = "user"
        resolver: Type[UserResolver]

        # models
        add_model: Type[AddUserInput] = AddUserInput
        patch_model: Type[UserPatch] = UserPatch
        ref_model: Type[UserRef] = UserRef

        # functions
        get_function_name: str = "getUser"
        query_function_name: str = "queryUser"

        add_function_name: str = "addUser"
        update_function_name: str = "updateUser"
        delete_function_name: str = "deleteUser"

        url: str = "https://sparkling-butterfly.us-east-1.aws.cloud.dgraph.io/graphql"
        uid_field_name: str = "id"


class UserGetParams(Params):
    id: Optional[str] = None
    slug: Optional[str] = None


class UserQueryParams(Params):
    filter: Optional[UserFilter] = None
    order: Optional[UserOrder] = None
    first: Optional[int] = None
    offset: Optional[int] = None


class UserEdges(BaseModel):
    artists: Optional[ArtistResolver] = None
    venues: Optional[VenueResolver] = None
    created_bookings: Optional[BookingResolver] = None
    artistsAggregate: Optional[ArtistAggregateResultResolver] = None
    venuesAggregate: Optional[VenueAggregateResultResolver] = None
    created_bookingsAggregate: Optional[BookingAggregateResultResolver] = None


class UserResolver(Resolver[User]):
    node: ClassVar[Type[User]] = User
    edges: UserEdges = Field(default_factory=UserEdges)
    query_params: UserQueryParams = Field(default_factory=UserQueryParams)

    async def get(
        self, id: Optional[str] = None, slug: Optional[str] = None
    ) -> Optional[User]:
        return await self._get({"id": id, "slug": slug})

    async def gerror(
        self, id: Optional[str] = None, slug: Optional[str] = None
    ) -> User:
        node = await self.get(id=id, slug=slug)
        if not node:
            raise GQLException(f"No User with {id=} and {slug=}")
        return node

    def filter(self, filter: Optional[UserFilter] = None, /) -> UserResolver:
        self.query_params.filter = filter
        return self

    def order(self, order: Optional[UserOrder] = None, /) -> UserResolver:
        self.query_params.order = order
        return self

    def first(self, first: Optional[int] = None, /) -> UserResolver:
        self.query_params.first = first
        return self

    def offset(self, offset: Optional[int] = None, /) -> UserResolver:
        self.query_params.offset = offset
        return self

    def artists(self, _: Optional[ArtistResolver] = None, /) -> UserResolver:
        self.edges.artists = _ or ArtistResolver()
        return self

    def venues(self, _: Optional[VenueResolver] = None, /) -> UserResolver:
        self.edges.venues = _ or VenueResolver()
        return self

    def created_bookings(self, _: Optional[BookingResolver] = None, /) -> UserResolver:
        self.edges.created_bookings = _ or BookingResolver()
        return self

    def artistsAggregate(
        self, _: Optional[ArtistAggregateResultResolver] = None, /
    ) -> UserResolver:
        self.edges.artistsAggregate = _ or ArtistAggregateResultResolver()
        return self

    def venuesAggregate(
        self, _: Optional[VenueAggregateResultResolver] = None, /
    ) -> UserResolver:
        self.edges.venuesAggregate = _ or VenueAggregateResultResolver()
        return self

    def created_bookingsAggregate(
        self, _: Optional[BookingAggregateResultResolver] = None, /
    ) -> UserResolver:
        self.edges.created_bookingsAggregate = _ or BookingAggregateResultResolver()
        return self


User.GQL.resolver = UserResolver


class UserAggregateResult(Node):
    count: Optional[int] = Field(None, allow_mutation=True)
    idMin: Optional[str] = Field(None, allow_mutation=True)
    idMax: Optional[str] = Field(None, allow_mutation=True)
    slugMin: Optional[str] = Field(None, allow_mutation=True)
    slugMax: Optional[str] = Field(None, allow_mutation=True)
    nameMin: Optional[str] = Field(None, allow_mutation=True)
    nameMax: Optional[str] = Field(None, allow_mutation=True)

    class GQL:
        typename = "UserAggregateResult"
        payload_node_name = None
        resolver: Type[None]

        # models
        add_model: Type[None] = None
        patch_model: Type[None] = None
        ref_model: Type[None] = None

        # functions
        get_function_name: str = "aggregateUser"
        query_function_name: str = None

        add_function_name: str = None
        update_function_name: str = None
        delete_function_name: str = None

        url: str = "https://sparkling-butterfly.us-east-1.aws.cloud.dgraph.io/graphql"
        uid_field_name: str = "count"


class UserAggregateResultGetParams(Params):
    filter: Optional[UserFilter] = None


class UserAggregateResultQueryParams(Params):
    pass


class UserAggregateResultEdges(BaseModel):
    pass


class UserAggregateResultResolver(Resolver[UserAggregateResult]):
    node: ClassVar[Type[UserAggregateResult]] = UserAggregateResult
    edges: UserAggregateResultEdges = Field(default_factory=UserAggregateResultEdges)
    query_params: UserAggregateResultQueryParams = Field(
        default_factory=UserAggregateResultQueryParams
    )

    async def get(
        self, filter: Optional[UserFilter] = None
    ) -> Optional[UserAggregateResult]:
        return await self._get({"filter": filter})

    async def gerror(self, filter: Optional[UserFilter] = None) -> UserAggregateResult:
        node = await self.get(filter=filter)
        if not node:
            raise GQLException(f"No UserAggregateResult with {filter=}")
        return node


UserAggregateResult.GQL.resolver = UserAggregateResultResolver


class Venue(Node):
    id: str = Field(..., allow_mutation=False)
    slug: str = Field(..., allow_mutation=False)
    name: str = Field(..., allow_mutation=True)

    async def owners(
        self,
        resolver: UserResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> List[Optional[User]]:
        return await self.resolve(
            name="owners", resolver=resolver, refresh=refresh, use_stale=use_stale
        )

    async def bookings(
        self,
        resolver: BookingResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> List[Optional[Booking]]:
        return await self.resolve(
            name="bookings", resolver=resolver, refresh=refresh, use_stale=use_stale
        )

    async def ownersAggregate(
        self,
        resolver: UserAggregateResultResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> Optional[UserAggregateResult]:
        return await self.resolve(
            name="ownersAggregate",
            resolver=resolver,
            refresh=refresh,
            use_stale=use_stale,
        )

    async def bookingsAggregate(
        self,
        resolver: BookingAggregateResultResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> Optional[BookingAggregateResult]:
        return await self.resolve(
            name="bookingsAggregate",
            resolver=resolver,
            refresh=refresh,
            use_stale=use_stale,
        )

    @classmethod
    async def add(
        cls,
        *,
        input: AddVenueInput,
        resolver: VenueResolver = None,
        upsert: bool = False,
    ) -> Venue:
        return await cls._add(input=input, given_resolver=resolver, upsert=upsert)

    async def update(
        self,
        resolver: VenueResolver = None,
        owners: List[Optional[User]] = None,
        remove_owners: List[Optional[User]] = None,
        bookings: List[Optional[Booking]] = None,
        remove_bookings: List[Optional[Booking]] = None,
    ) -> bool:
        return await self._update(
            given_resolver=resolver,
            to_set={"owners": owners, "bookings": bookings},
            to_remove={"owners": remove_owners, "bookings": remove_bookings},
        )

    class GQL:
        typename = "Venue"
        payload_node_name = "venue"
        resolver: Type[VenueResolver]

        # models
        add_model: Type[AddVenueInput] = AddVenueInput
        patch_model: Type[VenuePatch] = VenuePatch
        ref_model: Type[VenueRef] = VenueRef

        # functions
        get_function_name: str = "getVenue"
        query_function_name: str = "queryVenue"

        add_function_name: str = "addVenue"
        update_function_name: str = "updateVenue"
        delete_function_name: str = "deleteVenue"

        url: str = "https://sparkling-butterfly.us-east-1.aws.cloud.dgraph.io/graphql"
        uid_field_name: str = "id"


class VenueGetParams(Params):
    id: Optional[str] = None
    slug: Optional[str] = None


class VenueQueryParams(Params):
    filter: Optional[VenueFilter] = None
    order: Optional[VenueOrder] = None
    first: Optional[int] = None
    offset: Optional[int] = None


class VenueEdges(BaseModel):
    owners: Optional[UserResolver] = None
    bookings: Optional[BookingResolver] = None
    ownersAggregate: Optional[UserAggregateResultResolver] = None
    bookingsAggregate: Optional[BookingAggregateResultResolver] = None


class VenueResolver(Resolver[Venue]):
    node: ClassVar[Type[Venue]] = Venue
    edges: VenueEdges = Field(default_factory=VenueEdges)
    query_params: VenueQueryParams = Field(default_factory=VenueQueryParams)

    async def get(
        self, id: Optional[str] = None, slug: Optional[str] = None
    ) -> Optional[Venue]:
        return await self._get({"id": id, "slug": slug})

    async def gerror(
        self, id: Optional[str] = None, slug: Optional[str] = None
    ) -> Venue:
        node = await self.get(id=id, slug=slug)
        if not node:
            raise GQLException(f"No Venue with {id=} and {slug=}")
        return node

    def filter(self, filter: Optional[VenueFilter] = None, /) -> VenueResolver:
        self.query_params.filter = filter
        return self

    def order(self, order: Optional[VenueOrder] = None, /) -> VenueResolver:
        self.query_params.order = order
        return self

    def first(self, first: Optional[int] = None, /) -> VenueResolver:
        self.query_params.first = first
        return self

    def offset(self, offset: Optional[int] = None, /) -> VenueResolver:
        self.query_params.offset = offset
        return self

    def owners(self, _: Optional[UserResolver] = None, /) -> VenueResolver:
        self.edges.owners = _ or UserResolver()
        return self

    def bookings(self, _: Optional[BookingResolver] = None, /) -> VenueResolver:
        self.edges.bookings = _ or BookingResolver()
        return self

    def ownersAggregate(
        self, _: Optional[UserAggregateResultResolver] = None, /
    ) -> VenueResolver:
        self.edges.ownersAggregate = _ or UserAggregateResultResolver()
        return self

    def bookingsAggregate(
        self, _: Optional[BookingAggregateResultResolver] = None, /
    ) -> VenueResolver:
        self.edges.bookingsAggregate = _ or BookingAggregateResultResolver()
        return self


Venue.GQL.resolver = VenueResolver


class VenueAggregateResult(Node):
    count: Optional[int] = Field(None, allow_mutation=True)
    idMin: Optional[str] = Field(None, allow_mutation=True)
    idMax: Optional[str] = Field(None, allow_mutation=True)
    slugMin: Optional[str] = Field(None, allow_mutation=True)
    slugMax: Optional[str] = Field(None, allow_mutation=True)
    nameMin: Optional[str] = Field(None, allow_mutation=True)
    nameMax: Optional[str] = Field(None, allow_mutation=True)

    class GQL:
        typename = "VenueAggregateResult"
        payload_node_name = None
        resolver: Type[None]

        # models
        add_model: Type[None] = None
        patch_model: Type[None] = None
        ref_model: Type[None] = None

        # functions
        get_function_name: str = "aggregateVenue"
        query_function_name: str = None

        add_function_name: str = None
        update_function_name: str = None
        delete_function_name: str = None

        url: str = "https://sparkling-butterfly.us-east-1.aws.cloud.dgraph.io/graphql"
        uid_field_name: str = "count"


class VenueAggregateResultGetParams(Params):
    filter: Optional[VenueFilter] = None


class VenueAggregateResultQueryParams(Params):
    pass


class VenueAggregateResultEdges(BaseModel):
    pass


class VenueAggregateResultResolver(Resolver[VenueAggregateResult]):
    node: ClassVar[Type[VenueAggregateResult]] = VenueAggregateResult
    edges: VenueAggregateResultEdges = Field(default_factory=VenueAggregateResultEdges)
    query_params: VenueAggregateResultQueryParams = Field(
        default_factory=VenueAggregateResultQueryParams
    )

    async def get(
        self, filter: Optional[VenueFilter] = None
    ) -> Optional[VenueAggregateResult]:
        return await self._get({"filter": filter})

    async def gerror(
        self, filter: Optional[VenueFilter] = None
    ) -> VenueAggregateResult:
        node = await self.get(filter=filter)
        if not node:
            raise GQLException(f"No VenueAggregateResult with {filter=}")
        return node


VenueAggregateResult.GQL.resolver = VenueAggregateResultResolver


class Booking(Node):
    id: str = Field(..., allow_mutation=False)
    created_at: datetime = Field(..., allow_mutation=True)
    status: str = Field(..., allow_mutation=True)

    async def artist(
        self,
        resolver: ArtistResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> Artist:
        return await self.resolve(
            name="artist", resolver=resolver, refresh=refresh, use_stale=use_stale
        )

    async def venue(
        self,
        resolver: VenueResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> Venue:
        return await self.resolve(
            name="venue", resolver=resolver, refresh=refresh, use_stale=use_stale
        )

    async def created_by(
        self,
        resolver: UserResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> Optional[User]:
        return await self.resolve(
            name="created_by", resolver=resolver, refresh=refresh, use_stale=use_stale
        )

    @classmethod
    async def add(
        cls,
        *,
        input: AddBookingInput,
        resolver: BookingResolver = None,
        upsert: bool = False,
    ) -> Booking:
        return await cls._add(input=input, given_resolver=resolver, upsert=upsert)

    async def update(
        self,
        resolver: BookingResolver = None,
        artist: Artist = None,
        venue: Venue = None,
        created_by: Optional[User] = None,
        remove_created_by: Optional[User] = None,
    ) -> bool:
        return await self._update(
            given_resolver=resolver,
            to_set={"artist": artist, "venue": venue, "created_by": created_by},
            to_remove={"created_by": remove_created_by},
        )

    class GQL:
        typename = "Booking"
        payload_node_name = "booking"
        resolver: Type[BookingResolver]

        # models
        add_model: Type[AddBookingInput] = AddBookingInput
        patch_model: Type[BookingPatch] = BookingPatch
        ref_model: Type[BookingRef] = BookingRef

        # functions
        get_function_name: str = "getBooking"
        query_function_name: str = "queryBooking"

        add_function_name: str = "addBooking"
        update_function_name: str = "updateBooking"
        delete_function_name: str = "deleteBooking"

        url: str = "https://sparkling-butterfly.us-east-1.aws.cloud.dgraph.io/graphql"
        uid_field_name: str = "id"


class BookingGetParams(Params):
    id: str


class BookingQueryParams(Params):
    filter: Optional[BookingFilter] = None
    order: Optional[BookingOrder] = None
    first: Optional[int] = None
    offset: Optional[int] = None


class BookingEdges(BaseModel):
    artist: Optional[ArtistResolver] = None
    venue: Optional[VenueResolver] = None
    created_by: Optional[UserResolver] = None


class BookingResolver(Resolver[Booking]):
    node: ClassVar[Type[Booking]] = Booking
    edges: BookingEdges = Field(default_factory=BookingEdges)
    query_params: BookingQueryParams = Field(default_factory=BookingQueryParams)

    async def get(self, id: str) -> Optional[Booking]:
        return await self._get({"id": id})

    async def gerror(self, id: str) -> Booking:
        node = await self.get(id=id)
        if not node:
            raise GQLException(f"No Booking with {id=}")
        return node

    def filter(self, filter: Optional[BookingFilter] = None, /) -> BookingResolver:
        self.query_params.filter = filter
        return self

    def order(self, order: Optional[BookingOrder] = None, /) -> BookingResolver:
        self.query_params.order = order
        return self

    def first(self, first: Optional[int] = None, /) -> BookingResolver:
        self.query_params.first = first
        return self

    def offset(self, offset: Optional[int] = None, /) -> BookingResolver:
        self.query_params.offset = offset
        return self

    def artist(self, _: Optional[ArtistResolver] = None, /) -> BookingResolver:
        self.edges.artist = _ or ArtistResolver()
        return self

    def venue(self, _: Optional[VenueResolver] = None, /) -> BookingResolver:
        self.edges.venue = _ or VenueResolver()
        return self

    def created_by(self, _: Optional[UserResolver] = None, /) -> BookingResolver:
        self.edges.created_by = _ or UserResolver()
        return self


Booking.GQL.resolver = BookingResolver


class BookingAggregateResult(Node):
    count: Optional[int] = Field(None, allow_mutation=True)
    idMin: Optional[str] = Field(None, allow_mutation=True)
    idMax: Optional[str] = Field(None, allow_mutation=True)
    created_atMin: Optional[datetime] = Field(None, allow_mutation=True)
    created_atMax: Optional[datetime] = Field(None, allow_mutation=True)
    statusMin: Optional[str] = Field(None, allow_mutation=True)
    statusMax: Optional[str] = Field(None, allow_mutation=True)

    class GQL:
        typename = "BookingAggregateResult"
        payload_node_name = None
        resolver: Type[None]

        # models
        add_model: Type[None] = None
        patch_model: Type[None] = None
        ref_model: Type[None] = None

        # functions
        get_function_name: str = "aggregateBooking"
        query_function_name: str = None

        add_function_name: str = None
        update_function_name: str = None
        delete_function_name: str = None

        url: str = "https://sparkling-butterfly.us-east-1.aws.cloud.dgraph.io/graphql"
        uid_field_name: str = "count"


class BookingAggregateResultGetParams(Params):
    filter: Optional[BookingFilter] = None


class BookingAggregateResultQueryParams(Params):
    pass


class BookingAggregateResultEdges(BaseModel):
    pass


class BookingAggregateResultResolver(Resolver[BookingAggregateResult]):
    node: ClassVar[Type[BookingAggregateResult]] = BookingAggregateResult
    edges: BookingAggregateResultEdges = Field(
        default_factory=BookingAggregateResultEdges
    )
    query_params: BookingAggregateResultQueryParams = Field(
        default_factory=BookingAggregateResultQueryParams
    )

    async def get(
        self, filter: Optional[BookingFilter] = None
    ) -> Optional[BookingAggregateResult]:
        return await self._get({"filter": filter})

    async def gerror(
        self, filter: Optional[BookingFilter] = None
    ) -> BookingAggregateResult:
        node = await self.get(filter=filter)
        if not node:
            raise GQLException(f"No BookingAggregateResult with {filter=}")
        return node


BookingAggregateResult.GQL.resolver = BookingAggregateResultResolver


class Artist(Node):
    id: str = Field(..., allow_mutation=False)
    slug: str = Field(..., allow_mutation=False)
    name: str = Field(..., allow_mutation=True)

    async def sellers(
        self,
        resolver: UserResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> List[Optional[User]]:
        return await self.resolve(
            name="sellers", resolver=resolver, refresh=refresh, use_stale=use_stale
        )

    async def bookings(
        self,
        resolver: BookingResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> List[Optional[Booking]]:
        return await self.resolve(
            name="bookings", resolver=resolver, refresh=refresh, use_stale=use_stale
        )

    async def sellersAggregate(
        self,
        resolver: UserAggregateResultResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> Optional[UserAggregateResult]:
        return await self.resolve(
            name="sellersAggregate",
            resolver=resolver,
            refresh=refresh,
            use_stale=use_stale,
        )

    async def bookingsAggregate(
        self,
        resolver: BookingAggregateResultResolver = None,
        refresh: bool = False,
        use_stale: bool = False,
    ) -> Optional[BookingAggregateResult]:
        return await self.resolve(
            name="bookingsAggregate",
            resolver=resolver,
            refresh=refresh,
            use_stale=use_stale,
        )

    @classmethod
    async def add(
        cls,
        *,
        input: AddArtistInput,
        resolver: ArtistResolver = None,
        upsert: bool = False,
    ) -> Artist:
        return await cls._add(input=input, given_resolver=resolver, upsert=upsert)

    async def update(
        self,
        resolver: ArtistResolver = None,
        sellers: List[Optional[User]] = None,
        remove_sellers: List[Optional[User]] = None,
        bookings: List[Optional[Booking]] = None,
        remove_bookings: List[Optional[Booking]] = None,
    ) -> bool:
        return await self._update(
            given_resolver=resolver,
            to_set={"sellers": sellers, "bookings": bookings},
            to_remove={"sellers": remove_sellers, "bookings": remove_bookings},
        )

    class GQL:
        typename = "Artist"
        payload_node_name = "artist"
        resolver: Type[ArtistResolver]

        # models
        add_model: Type[AddArtistInput] = AddArtistInput
        patch_model: Type[ArtistPatch] = ArtistPatch
        ref_model: Type[ArtistRef] = ArtistRef

        # functions
        get_function_name: str = "getArtist"
        query_function_name: str = "queryArtist"

        add_function_name: str = "addArtist"
        update_function_name: str = "updateArtist"
        delete_function_name: str = "deleteArtist"

        url: str = "https://sparkling-butterfly.us-east-1.aws.cloud.dgraph.io/graphql"
        uid_field_name: str = "id"


class ArtistGetParams(Params):
    id: Optional[str] = None
    slug: Optional[str] = None


class ArtistQueryParams(Params):
    filter: Optional[ArtistFilter] = None
    order: Optional[ArtistOrder] = None
    first: Optional[int] = None
    offset: Optional[int] = None


class ArtistEdges(BaseModel):
    sellers: Optional[UserResolver] = None
    bookings: Optional[BookingResolver] = None
    sellersAggregate: Optional[UserAggregateResultResolver] = None
    bookingsAggregate: Optional[BookingAggregateResultResolver] = None


class ArtistResolver(Resolver[Artist]):
    node: ClassVar[Type[Artist]] = Artist
    edges: ArtistEdges = Field(default_factory=ArtistEdges)
    query_params: ArtistQueryParams = Field(default_factory=ArtistQueryParams)

    async def get(
        self, id: Optional[str] = None, slug: Optional[str] = None
    ) -> Optional[Artist]:
        return await self._get({"id": id, "slug": slug})

    async def gerror(
        self, id: Optional[str] = None, slug: Optional[str] = None
    ) -> Artist:
        node = await self.get(id=id, slug=slug)
        if not node:
            raise GQLException(f"No Artist with {id=} and {slug=}")
        return node

    def filter(self, filter: Optional[ArtistFilter] = None, /) -> ArtistResolver:
        self.query_params.filter = filter
        return self

    def order(self, order: Optional[ArtistOrder] = None, /) -> ArtistResolver:
        self.query_params.order = order
        return self

    def first(self, first: Optional[int] = None, /) -> ArtistResolver:
        self.query_params.first = first
        return self

    def offset(self, offset: Optional[int] = None, /) -> ArtistResolver:
        self.query_params.offset = offset
        return self

    def sellers(self, _: Optional[UserResolver] = None, /) -> ArtistResolver:
        self.edges.sellers = _ or UserResolver()
        return self

    def bookings(self, _: Optional[BookingResolver] = None, /) -> ArtistResolver:
        self.edges.bookings = _ or BookingResolver()
        return self

    def sellersAggregate(
        self, _: Optional[UserAggregateResultResolver] = None, /
    ) -> ArtistResolver:
        self.edges.sellersAggregate = _ or UserAggregateResultResolver()
        return self

    def bookingsAggregate(
        self, _: Optional[BookingAggregateResultResolver] = None, /
    ) -> ArtistResolver:
        self.edges.bookingsAggregate = _ or BookingAggregateResultResolver()
        return self


Artist.GQL.resolver = ArtistResolver


class ArtistAggregateResult(Node):
    count: Optional[int] = Field(None, allow_mutation=True)
    idMin: Optional[str] = Field(None, allow_mutation=True)
    idMax: Optional[str] = Field(None, allow_mutation=True)
    slugMin: Optional[str] = Field(None, allow_mutation=True)
    slugMax: Optional[str] = Field(None, allow_mutation=True)
    nameMin: Optional[str] = Field(None, allow_mutation=True)
    nameMax: Optional[str] = Field(None, allow_mutation=True)

    class GQL:
        typename = "ArtistAggregateResult"
        payload_node_name = None
        resolver: Type[None]

        # models
        add_model: Type[None] = None
        patch_model: Type[None] = None
        ref_model: Type[None] = None

        # functions
        get_function_name: str = "aggregateArtist"
        query_function_name: str = None

        add_function_name: str = None
        update_function_name: str = None
        delete_function_name: str = None

        url: str = "https://sparkling-butterfly.us-east-1.aws.cloud.dgraph.io/graphql"
        uid_field_name: str = "count"


class ArtistAggregateResultGetParams(Params):
    filter: Optional[ArtistFilter] = None


class ArtistAggregateResultQueryParams(Params):
    pass


class ArtistAggregateResultEdges(BaseModel):
    pass


class ArtistAggregateResultResolver(Resolver[ArtistAggregateResult]):
    node: ClassVar[Type[ArtistAggregateResult]] = ArtistAggregateResult
    edges: ArtistAggregateResultEdges = Field(
        default_factory=ArtistAggregateResultEdges
    )
    query_params: ArtistAggregateResultQueryParams = Field(
        default_factory=ArtistAggregateResultQueryParams
    )

    async def get(
        self, filter: Optional[ArtistFilter] = None
    ) -> Optional[ArtistAggregateResult]:
        return await self._get({"filter": filter})

    async def gerror(
        self, filter: Optional[ArtistFilter] = None
    ) -> ArtistAggregateResult:
        node = await self.get(filter=filter)
        if not node:
            raise GQLException(f"No ArtistAggregateResult with {filter=}")
        return node


ArtistAggregateResult.GQL.resolver = ArtistAggregateResultResolver


class BeatGigArtist(Node):
    id: str = Field(..., allow_mutation=True)
    slug: str = Field(..., allow_mutation=False)
    name: str = Field(..., allow_mutation=True)

    class GQL:
        typename = "BeatGigArtist"
        payload_node_name = None
        resolver: Type[None]

        # models
        add_model: Type[None] = None
        patch_model: Type[None] = None
        ref_model: Type[None] = None

        # functions
        get_function_name: str = "getArtistBeatGig"
        query_function_name: str = None

        add_function_name: str = None
        update_function_name: str = None
        delete_function_name: str = None

        url: str = "https://sparkling-butterfly.us-east-1.aws.cloud.dgraph.io/graphql"
        uid_field_name: str = "id"


class BeatGigArtistGetParams(Params):
    slug: str


class BeatGigArtistQueryParams(Params):
    pass


class BeatGigArtistEdges(BaseModel):
    pass


class BeatGigArtistResolver(Resolver[BeatGigArtist]):
    node: ClassVar[Type[BeatGigArtist]] = BeatGigArtist
    edges: BeatGigArtistEdges = Field(default_factory=BeatGigArtistEdges)
    query_params: BeatGigArtistQueryParams = Field(
        default_factory=BeatGigArtistQueryParams
    )

    async def get(self, slug: str) -> Optional[BeatGigArtist]:
        return await self._get({"slug": slug})

    async def gerror(self, slug: str) -> BeatGigArtist:
        node = await self.get(slug=slug)
        if not node:
            raise GQLException(f"No BeatGigArtist with {slug=}")
        return node


BeatGigArtist.GQL.resolver = BeatGigArtistResolver


AddArtistInput.update_forward_refs()
AddBookingInput.update_forward_refs()
AddStudentInput.update_forward_refs()
AddTeacherInput.update_forward_refs()
AddUserInput.update_forward_refs()
AddVenueInput.update_forward_refs()
ArtistFilter.update_forward_refs()
ArtistOrder.update_forward_refs()
ArtistPatch.update_forward_refs()
ArtistRef.update_forward_refs()
AuthRule.update_forward_refs()
BookingFilter.update_forward_refs()
BookingOrder.update_forward_refs()
BookingPatch.update_forward_refs()
BookingRef.update_forward_refs()
ContainsFilter.update_forward_refs()
CustomHTTP.update_forward_refs()
DateTimeFilter.update_forward_refs()
DateTimeRange.update_forward_refs()
FloatFilter.update_forward_refs()
FloatRange.update_forward_refs()
GenerateMutationParams.update_forward_refs()
GenerateQueryParams.update_forward_refs()
Int64Filter.update_forward_refs()
Int64Range.update_forward_refs()
IntersectsFilter.update_forward_refs()
IntFilter.update_forward_refs()
IntRange.update_forward_refs()
MultiPolygonRef.update_forward_refs()
NearFilter.update_forward_refs()
PointGeoFilter.update_forward_refs()
PointListRef.update_forward_refs()
PointRef.update_forward_refs()
PolygonGeoFilter.update_forward_refs()
PolygonRef.update_forward_refs()
StringExactFilter.update_forward_refs()
StringFullTextFilter.update_forward_refs()
StringFullTextFilter_StringRegExpFilter_StringTermFilter.update_forward_refs()
StringHashFilter.update_forward_refs()
StringRange.update_forward_refs()
StringRegExpFilter.update_forward_refs()
StringTermFilter.update_forward_refs()
StudentFilter.update_forward_refs()
StudentOrder.update_forward_refs()
StudentPatch.update_forward_refs()
StudentRef.update_forward_refs()
TeacherFilter.update_forward_refs()
TeacherOrder.update_forward_refs()
TeacherPatch.update_forward_refs()
TeacherRef.update_forward_refs()
UpdateArtistInput.update_forward_refs()
UpdateBookingInput.update_forward_refs()
UpdateStudentInput.update_forward_refs()
UpdateTeacherInput.update_forward_refs()
UpdateUserInput.update_forward_refs()
UpdateVenueInput.update_forward_refs()
UserFilter.update_forward_refs()
UserOrder.update_forward_refs()
UserPatch.update_forward_refs()
UserRef.update_forward_refs()
VenueFilter.update_forward_refs()
VenueOrder.update_forward_refs()
VenuePatch.update_forward_refs()
VenueRef.update_forward_refs()
WithinFilter.update_forward_refs()

AddArtistPayload.update_forward_refs()
AddBookingPayload.update_forward_refs()
AddStudentPayload.update_forward_refs()
AddTeacherPayload.update_forward_refs()
AddUserPayload.update_forward_refs()
AddVenuePayload.update_forward_refs()
DeleteArtistPayload.update_forward_refs()
DeleteBookingPayload.update_forward_refs()
DeleteStudentPayload.update_forward_refs()
DeleteTeacherPayload.update_forward_refs()
DeleteUserPayload.update_forward_refs()
DeleteVenuePayload.update_forward_refs()
MultiPolygon.update_forward_refs()
Point.update_forward_refs()
PointList.update_forward_refs()
Polygon.update_forward_refs()
UpdateArtistPayload.update_forward_refs()
UpdateBookingPayload.update_forward_refs()
UpdateStudentPayload.update_forward_refs()
UpdateTeacherPayload.update_forward_refs()
UpdateUserPayload.update_forward_refs()
UpdateVenuePayload.update_forward_refs()

StudentEdges.update_forward_refs()
StudentAggregateResultEdges.update_forward_refs()
TeacherEdges.update_forward_refs()
TeacherAggregateResultEdges.update_forward_refs()
UserEdges.update_forward_refs()
UserAggregateResultEdges.update_forward_refs()
VenueEdges.update_forward_refs()
VenueAggregateResultEdges.update_forward_refs()
BookingEdges.update_forward_refs()
BookingAggregateResultEdges.update_forward_refs()
ArtistEdges.update_forward_refs()
ArtistAggregateResultEdges.update_forward_refs()
BeatGigArtistEdges.update_forward_refs()

Student.update_forward_refs()
StudentAggregateResult.update_forward_refs()
Teacher.update_forward_refs()
TeacherAggregateResult.update_forward_refs()
User.update_forward_refs()
UserAggregateResult.update_forward_refs()
Venue.update_forward_refs()
VenueAggregateResult.update_forward_refs()
Booking.update_forward_refs()
BookingAggregateResult.update_forward_refs()
Artist.update_forward_refs()
ArtistAggregateResult.update_forward_refs()
BeatGigArtist.update_forward_refs()
