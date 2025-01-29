import requests
import time

def test_download_speed(url):
    """
    Tests download speed by downloading a file from the given URL.

    Args:
        url (str): The URL of the file to download for testing.

    Returns:
        tuple: A tuple containing download speed in Mbps and MB/s, or None if an error occurs.
    """
    try:
        start_time = time.time()
        response = requests.get(url, stream=True)  # stream=True for large files
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        total_size_in_bytes = int(response.headers.get('content-length', 0))
        if total_size_in_bytes == 0:
            print("Warning: Could not determine file size from headers. Speed might be inaccurate.")
            total_size_in_bytes = 1  # Avoid division by zero if size is unknown

        downloaded_bytes = 0
        for chunk in response.iter_content(chunk_size=8192): # 8KB chunks
            downloaded_bytes += len(chunk)

        end_time = time.time()
        download_time = end_time - start_time

        if download_time == 0:
            return None  # Avoid division by zero if download is too fast

        speed_bps = (downloaded_bytes * 8) / download_time  # bits per second
        speed_mbps = speed_bps / (1000 * 1000)  # Megabits per second
        speed_mbs = downloaded_bytes / download_time / (1000 * 1000) # Megabytes per second

        return speed_mbps, speed_mbs

    except requests.exceptions.RequestException as e:
        print(f"Error during download test: {e}")
        return None

if __name__ == "__main__":
    test_file_url = "http://speedtest.tele2.net/100MB.zip"  # Example 10MB file
    print(f"Testing download speed using file: {test_file_url}")

    speed_results = test_download_speed(test_file_url)

    if speed_results:
        mbps_speed, mbs_speed = speed_results
        print(f"Download Speed: {mbps_speed:.2f} Mbps")
        print(f"Download Speed: {mbs_speed:.2f} MB/s")
    else:
        print("Download speed test failed.")