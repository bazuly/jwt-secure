import asyncio
import aiohttp
import json
import time


async def test_token_blacklist():
    base_url = "http://localhost:8000"

    timestamp = int(time.time())
    unique_username = f"test_user_{timestamp}"
    unique_content_name = f"test_private_{timestamp}"

    async with aiohttp.ClientSession() as session:
        register_data = {
            "username": unique_username,
            "password": "test_password",
            "access_level": "private"
        }
        async with session.post(f"{base_url}/users/register", json=register_data) as response:
            print("Register response:", await response.text())
            if response.status == 200:
                register_result = await response.json()
                access_token = register_result["access_token"]
                print(f"Got access token: {access_token}")
            else:
                print(f"Registration failed with status {response.status}")
                return

        content_data = {
            "content_name": unique_content_name,
            "content_data": "private content",
            "access_level": "private"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        async with session.post(f"{base_url}/content/create", json=content_data, headers=headers) as response:
            print("Create content response:", await response.text())
            if response.status != 200:
                print(f"Content creation failed with status {response.status}")
                return

        # Симуляция разных IP
        print("\nMaking first request (should succeed):")
        params = {
            "content_name": unique_content_name,
            "access_token": access_token
        }
        async with session.get(
            f"{base_url}/content/get_content/{unique_content_name}",
            params=params
        ) as response:
            print(f"First request status: {response.status}")
            print("Response:", await response.text())

        print("\nMaking second request with different IP (should fail):")
        headers["X-Forwarded-For"] = "1.2.3.4"
        async with session.get(
            f"{base_url}/content/get_content/{unique_content_name}",
            params=params,
            headers=headers
        ) as response:
            print(f"Second request status: {response.status}")
            print("Response:", await response.text())

        print("\nMaking third request with original IP (should fail due to blacklist):")
        headers.pop("X-Forwarded-For", None)
        async with session.get(
            f"{base_url}/content/get_content/{unique_content_name}",
            params=params,
            headers=headers
        ) as response:
            print(f"Third request status: {response.status}")
            print("Response:", await response.text())

if __name__ == "__main__":
    asyncio.run(test_token_blacklist())
