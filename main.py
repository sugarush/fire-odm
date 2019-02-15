import asyncio

from user import Type, User

async def seed():
    type = await Type.add({
        'name': 'administrator'
    })

    models = await User.add([
        {
            'name': {
                'first': 'paul',
                'last': 'severance'
            },
            'type': type.id
        },
        {
            'name': {
                'first': 'alice',
                'last': 'jane'
            },
            'type': type.id
        }
    ])

async def main():

    await Type.drop()
    await User.drop()

    await seed()

    async for user in User.find():
        print(user)
        type = await Type.find_by_id(user.type)
        print(type)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
