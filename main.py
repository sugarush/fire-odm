import asyncio

from user import User

async def seed():
    
    models = await User.add([
        {
            'name': {
                'first': 'paul',
                'last': 'severance'
            }
        },
        {
            'name': {
                'first': 'alice',
                'last': 'jane'
            }
        }
    ])

async def main():

    await User.drop()

    await seed()

    async for user in User.find():
        print(user)
        await user.delete()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
