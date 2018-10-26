import asyncio

from user import User

async def seed():
    models, errors = await User.add([
        {
            'id': '1',
            'name': {
                'first': 'paul',
                'last': 'severance'
            }
        },
        {
            'id': '2',
            'name': {
                'first': 'alice',
                'last': 'jane'
            }
        }
    ])

    if models:
        for model in models:
            print(model)

    if errors:
        for error in errors:
            print(error)

async def main(loop):

    await User.drop()

    await seed()

    async for user in User.find():
        await user.save()
        #print(user.to_jsonapi())

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main(loop))
