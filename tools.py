import asyncio, re, random, aiohttp, uuid, os
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import pyshorteners, humanfriendly
import pyrogram, asyncio, os, uvloop, uuid, random, subprocess, requests
import re, json, aiohttp, random
from urllib.parse import parse_qs, urlparse
from io import BytesIO

#loop = asyncio.get_event_loop()
rapi = pyshorteners.Shortener()

download_urls = ["https://d3.terabox.app", "https://d3.1024tera.com", "https://d4.terabox.app", "https://d4.1024tera.com", "https://d5.terabox.app", "https://d5.1024tera.com"]

cookie = 'browserid=khXCS03TzvdACGfWjfD-9fdJBWCd83okmrk0apGAEPjCXVWWeTWXwdqk0fU=; lang=en; __bid_n=18e3dd5bb2c9cb73434207; _ga=GA1.1.1811415982.1710434419; __stripe_mid=759ba489-0c3b-40da-a098-dd7ab307d05c9f299d; __bid_n=18e8bfdfc3be4ea4224207; csrfToken=8JPIz5vKB7OFpUJPYTiUzWtW; ndus=Y23AA8KteHuisa-G0gHj13u4hy-0jpGBB1qMIP6j; ndut_fmt=068CF73643C0A6D33CA63114B295CD291FAE96FC359C85F7B519B6EB40AD2769; ab_sr=1.0.1_Y2Q2NzFmMjJjZjI2ZTIwY2Y1OGRmMjdkYjQ4NDNkYWE5ZjM4N2YwNDM4MjViZThmZWNhMDczYWQxMDNlNjVhNmRhMjEwNWNhMDk0M2Q2YjkzOTcyNDk1MjY0MTYwYTJmMmU4ZTZjOWJhNzRiODkxZjRkYmUzODg0ZjRmZjgwMWUzYTViMzQ3NDBmMzQzMGRiZjg5ZWM3YWZlODUzMDdjYQ==; ab_ymg_result={"data":"eb84d2c1e0bdeab29071677f50331dcf2c3ec7fb62a3feafc0f94cccf1b1ccaa34c5bc0d95e6e60a6b02b3d1577127ebfe85ff48d0f62ecbd8c0fea8b5eb38bcffac8cd6e82103ef074257509767fcbb3cd5db615d54b0eebe88148f78b786a885cecadd43c7a3c60b0d6569bda8e2c9966b647c77cbd9f7c88421c1f557d8b7","key_id":"66","sign":"2e10ba72"}; _ga_06ZNKL8C2E=GS1.1.1711745818.2.1.1711746308.15.0.0'
        

async def update_progress(downloaded, total, message, state="Uploading"):
    try:
        percentage = (downloaded / total) * 100
        downloaded_str = humanfriendly.format_size(downloaded)
        total_str = humanfriendly.format_size(total)
        
        # Check if percentage is a multiple of 10
        if int(percentage) % 30 == 0:
            await message.edit_text(f"{state}: {downloaded_str} / {total_str} ({percentage:.0f}%)")
        
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        print(e)
        pass
      

"""
def download_file(url: str, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()        
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)                
        return filename
    except Exception as e:
        print(f"Error downloading file: {e}")
        try:
            os.remove(filename)
        except:
            pass
        return False
        
"""

def download_file(url, file_path, retry_count=0):    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))    
        with open(file_path, 'ab') as file:
            file.seek(0, os.SEEK_END) 
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    downloaded_size = file.tell()              
                    if downloaded_size >= total_size:
                        break
        return file_path 
    except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError) as e:
        if retry_count < 3: 
            print(f"Retrying... (Attempt {retry_count + 1})")
            return download_file(url, file_path, retry_count + 1)
        else:
            print("Maximum retry attempts reached.")
            try:
                os.remove(file_path)
            except:
                pass
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        try:
            os.remove(file_path)
        except:
            pass
        return None



def download_thumb(url: str):
    try:
        random_uuid = uuid.uuid4()
        uuid_string = str(random_uuid)
        filename = f"downloads/{uuid_string}.jpeg"
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename    
    except Exception as e:
        print(f"Error downloading image: {e}")
        try:
            os.remove(filename)
        except:
            pass
        return None


def get_duration(file_path):
    command = [
        "ffprobe",
        "-loglevel",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        file_path,
    ]

    pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = pipe.communicate()
    _json = json.loads(out)

    if "format" in _json:
        if "duration" in _json["format"]:
            return float(_json["format"]["duration"])

    if "streams" in _json:
        for s in _json["streams"]:
            if "duration" in s:
                print(float(s["duration"]))
                return float(s["duration"])

    return None


async def extract_link(message):
    try:
        url_pattern = r'https?://\S+'
        match = re.search(url_pattern, message)
        if match:
            first_url = match.group()
            return first_url
        else:
            return None
    except Exception as e:
     	print(e)
     	return None

                
async def extract_surl_from_url(url: str):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    surl = query_params.get("surl", [])

    if surl:
        return surl[0]
    else:
        return False
      
async def get_formatted_size_async(size_bytes):
    try:
        size_bytes = int(size_bytes)
        size = size_bytes / (1024 * 1024) if size_bytes >= 1024 * 1024 else (
            size_bytes / 1024 if size_bytes >= 1024 else size_bytes
        )
        unit = "MB" if size_bytes >= 1024 * 1024 else ("KB" if size_bytes >= 1024 else "bytes")

        return f"{size:.2f} {unit}"
    except Exception as e:
        print(f"Error getting formatted size: {e}")
        return None


async def check_url_patterns_async(url):
    patterns = [
        r"ww\.mirrobox\.com",
        r"www\.nephobox\.com",
        r"freeterabox\.com",
        r"www\.freeterabox\.com",
        r"1024tera\.com",
        r"4funbox\.co",
        r"www\.4funbox\.com",
        r"mirrobox\.com",
        r"nephobox\.com",
        r"terabox\.app",
        r"terabox\.com",
        r"www\.terabox\.ap",
        r"terabox\.fun",
        r"www\.terabox\.com",
        r"www\.1024tera\.co",
        r"www\.momerybox\.com",
        r"teraboxapp\.com",
        r"momerybox\.com",
        r"tibibox\.com",
        r"www\.tibibox\.com",
        r"www\.teraboxapp\.com",
    ]

    for pattern in patterns:
        if re.search(pattern, url):
            return True
    return False


async def find_between(string, start, end):
    start_index = string.find(start) + len(start)
    end_index = string.find(end, start_index)
    return string[start_index:end_index]

async def shorten_url(long_url):
    api_key = '26LFT5xlnvMbhEwux1LCDvftvss2'
    api_url = f"https://api.shareus.io/easy_api?key={api_key}&link={long_url}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.text()
                    return data.strip()  # Remove any extra whitespace
                else:
                    print(f"Failed to shorten URL. Status code: {response.status}")
                    return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
             
async def get_data(url: str):
    headersList = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "DNT": "1",
        "Host": "www.terabox.app",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headersList) as response:
            response_url = str(response.url)
            response_text = await response.text()

    logid = await find_between(response_text, "dp-logid=", "&")
    jsToken = await find_between(response_text, "fn%28%22", "%22%29")
    bdstoken = await find_between(response_text, 'bdstoken":"', '"')
    shorturl = await extract_surl_from_url(response_url)
    if not shorturl:
        return False

    reqUrl = f"https://www.terabox.app/share/list?app_id=250528&web=1&channel=0&jsToken={jsToken}&dp-logid={logid}&page=1&num=20&by=name&order=asc&site_referer=&shorturl={shorturl}&root=1"

    async with aiohttp.ClientSession() as session:
        async with session.get(reqUrl, headers=headersList) as response:
            if response.status != 200:
                return False
            r_j = await response.json()

    if r_j["errno"]:
        return False
    if "list" not in r_j or not r_j["list"]:
        return False

    async with aiohttp.ClientSession() as session:
        async with session.head(r_j["list"][0]["dlink"], headers=headersList) as response:
            direct_link = response.headers.get("location")
    tiny = rapi.tinyurl.short(direct_link)
    data = {
        "file_name": r_j["list"][0]["server_filename"],
        "link": r_j["list"][0]["dlink"],
        "direct_link": direct_link,
        "thumb": r_j["list"][0]["thumbs"]["url3"],
        "size": await get_formatted_size_async(int(r_j["list"][0]["size"])),
        "sizebytes": int(r_j["list"][0]["size"]),
        "tinyurl": tiny, 
    }
    return data['file_name'], data['direct_link'], data['thumb'], data['size'], data['sizebytes'], data['tinyurl']
     
