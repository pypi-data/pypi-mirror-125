from devtools import debug
import asyncio

from dgraph_orm.generator.node_testing import *

print(TeacherResolver.node)


async def run():
    teachers = await TeacherResolver().query()
    debug(teachers)

    students = (
        await StudentResolver()
        .filter(StudentFilter(has=[StudentHasFilter.favorite_artist_id]))
        .taught_by()
        .favorite_artist()
        .is_friends_withAggregate()
        .query()
    )
    debug(students)
    for student in students:
        fav_artist = await student.favorite_artist()
        print(fav_artist)
        # teacher = await student.taught_by()
        # print(teacher)
        print(await student.is_friends_withAggregate())


async def bleeding_edge():
    resolver = BeatGigArtistResolver()
    print(resolver)

    artist = await BeatGigArtistResolver().get(slug="cade")
    debug(artist)

    agg = await StudentAggregateResultResolver().get()
    debug(agg)
    try:
        await StudentAggregateResult().update()
    except Exception as e:
        assert type(e) is GQLException

    teach = await TeacherResolver().get()
    debug(teach)


StringHashFilter().in_ = ["Jeremy"]
StringHashFilter(in_=["jeremy", "zach"])


async def students():
    students = await (
        StudentResolver()
        .is_friends_with()
        .filter(StudentFilter(username=StringHashFilter(in_=["jeremy", "zach"])))
        .query()
    )
    debug(students)


async def new_models_testing():
    users = await UserResolver().artistsAggregate().query()
    for user in users:
        print(f"{user.name}, {await user.artistsAggregate()}")

    bookings = await BookingResolver().query()
    debug(bookings)


async def main():
    # await run()
    # await bleeding_edge()
    # await students()
    await new_models_testing()


if __name__ == "__main__":
    asyncio.run(main())
