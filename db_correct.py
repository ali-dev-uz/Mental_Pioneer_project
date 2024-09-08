import asyncio

from loader import db, dp


async def on_startup2():
    await db.create()
    await db.create_training_courses()
    await db.create_training_courses_arabic()
    # await db.drop_users()
    # await db.add_training_course(course_name="Guided Meditation",
    #                              course_id="course1",
    #                              course_price=999,
    #                              course_channel=-1002193321511)
    # await db.add_training_course(course_name="Holy Subliminal",
    #                              course_id="course2",
    #                              course_price=999,
    #                              course_channel=-1002246600813)
    # await db.add_training_course(course_name="Money Subliminal",
    #                              course_id="course3",
    #                              course_price=999,
    #                              course_channel=-1002215313141)
    # await db.add_training_course(course_name="Self Development Subliminal",
    #                              course_id="course4",
    #                              course_price=999,
    #                              course_channel=-1002216267911)
    await db.delete_training_course_arabic()
    await db.add_training_course_arabic(course_name="التأمل الموجه ",
                                        course_id="course1",
                                        course_price=999,
                                        course_channel=-1002245707991)
    await db.add_training_course_arabic(course_name="السبليمنال الديني",
                                        course_id="course2",
                                        course_price=999,
                                        course_channel=-1002213759182)
    await db.add_training_course_arabic(course_name="سبليمنال الثراء",
                                        course_id="course3",
                                        course_price=999,
                                        course_channel=-1002222132173)
    await db.add_training_course_arabic(course_name="سبليمنال تطوير الذات",
                                        course_id="course4",
                                        course_price=999,
                                        course_channel=-1002153988064)


if __name__ == '__main__':
    asyncio.run(on_startup2())
