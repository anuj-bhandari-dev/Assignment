# dummy email send
import asyncio


async def send_email(ctx, author_email: str):
    print(f"sending email to author_email {author_email}")
    await asyncio.sleep(5)
    return {"status": "sent", "author_email": author_email}
