import requests
from urllib.parse import urlparse
import re
from typing import Dict, Tuple


class Helper:

    @staticmethod
    def is_webpage_with_content(
        url: str, timeout: int = 10, min_content_length: int = 100
    ) -> Dict[str, any]:
        """
        Check if a URL is a webpage with actual content.

        Args:
            url: The URL to check
            timeout: Request timeout in seconds
            min_content_length: Minimum content length to consider as having content (bytes)

        Returns:
            Dictionary with check results and details
        """

        def validate_url_format(url: str) -> Tuple[str, bool]:
            """Validate and normalize URL format"""
            if not url:
                return url, False

            # Add scheme if missing
            if not re.match(r"^https?://", url, re.IGNORECASE):
                url = "https://" + url

            try:
                parsed = urlparse(url)
                if not parsed.netloc:
                    return url, False
                return url, True
            except:
                return url, False

        def is_likely_webpage_by_extension(url: str) -> bool:
            """Check if URL has common non-webpage file extensions"""
            non_webpage_extensions = [
                # Images
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".bmp",
                ".webp",
                ".svg",
                ".ico",
                ".tiff",
                # Documents
                ".pdf",
                ".doc",
                ".docx",
                ".txt",
                ".rtf",
                ".odt",
                ".ppt",
                ".pptx",
                ".xls",
                ".xlsx",
                # Archives
                ".zip",
                ".rar",
                ".7z",
                ".tar",
                ".gz",
                # Videos
                ".mp4",
                ".avi",
                ".mov",
                ".wmv",
                ".flv",
                ".webm",
                ".mkv",
                ".m4v",
                # Audio
                ".mp3",
                ".wav",
                ".ogg",
                ".flac",
                ".aac",
                ".m4a",
                # Other
                ".exe",
                ".dmg",
                ".pkg",
                ".deb",
                ".rpm",
            ]

            url_lower = url.lower()
            return not any(url_lower.endswith(ext) for ext in non_webpage_extensions)

        def is_webpage_content_type(content_type: str) -> bool:
            """Check if content type indicates a webpage"""
            if not content_type:
                return False

            webpage_content_types = [
                "text/html",
                "text/plain",
                "application/xhtml+xml",
                "application/json",
                "application/xml",
                "text/xml",
            ]

            content_type_lower = content_type.lower()

            # Exact matches
            if content_type_lower in webpage_content_types:
                return True

            # Partial matches
            if content_type_lower.startswith("text/"):
                return True

            return False

        # Main logic
        result = {
            "url": url,
            "is_webpage": False,
            "has_content": False,
            "content_type": None,
            "content_length": 0,
            "status_code": None,
            "error": None,
            "details": "",
        }

        try:
            # Step 1: Validate URL format
            normalized_url, is_valid = validate_url_format(url)
            if not is_valid:
                result["error"] = "Invalid URL format"
                result["details"] = "URL is malformed or missing domain"
                return result

            result["url"] = normalized_url

            # Step 2: Quick check based on file extension
            if not is_likely_webpage_by_extension(normalized_url):
                result["details"] = "URL has non-webpage file extension"
                return result

            # Step 3: Make HEAD request first to check content type
            try:
                head_response = requests.head(
                    normalized_url,
                    timeout=timeout,
                    allow_redirects=True,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    },
                )
                result["status_code"] = head_response.status_code

                # Check if status code indicates success
                if head_response.status_code != 200:
                    result["details"] = (
                        f"HTTP status {head_response.status_code} - not accessible"
                    )
                    return result

                content_type = head_response.headers.get("content-type", "").split(";")[
                    0
                ]
                result["content_type"] = content_type

                # Check if content type indicates webpage
                if not is_webpage_content_type(content_type):
                    result["details"] = (
                        f'Content type "{content_type}" is not a webpage'
                    )
                    return result

            except requests.exceptions.RequestException as e:
                result["error"] = f"HEAD request failed: {str(e)}"
                # Continue to try GET request as fallback

            # Step 4: Make GET request to verify content
            try:
                get_response = requests.get(
                    normalized_url,
                    timeout=timeout,
                    allow_redirects=True,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    },
                    stream=True,  # Stream to avoid downloading large files
                )

                result["status_code"] = get_response.status_code

                if get_response.status_code != 200:
                    result["details"] = (
                        f"HTTP status {get_response.status_code} - not accessible"
                    )
                    return result

                # Get content length
                content_length = get_response.headers.get("content-length")
                if content_length:
                    result["content_length"] = int(content_length)
                else:
                    # Read first few bytes to estimate content
                    chunk = get_response.content[:1024]
                    result["content_length"] = len(chunk)

                # Get actual content type from GET response
                content_type = get_response.headers.get("content-type", "").split(";")[
                    0
                ]
                result["content_type"] = content_type

                # Final verification
                is_webpage = is_webpage_content_type(content_type)
                has_content = result["content_length"] >= min_content_length

                result["is_webpage"] = is_webpage
                result["has_content"] = has_content

                if is_webpage and has_content:
                    result["details"] = (
                        f'Webpage with {result["content_length"]} bytes of content'
                    )
                elif is_webpage and not has_content:
                    result["details"] = "Webpage but little or no content"
                else:
                    result["details"] = f"Not a webpage (Content-Type: {content_type})"

            except requests.exceptions.RequestException as e:
                result["error"] = f"GET request failed: {str(e)}"
                result["details"] = "Failed to fetch content"

        except Exception as e:
            result["error"] = f"Unexpected error: {str(e)}"
            result["details"] = "Processing failed"

        return result

    @staticmethod
    def is_webpage(url: str, timeout: int = 5) -> bool:
        """Simple check if URL is a webpage (returns boolean only)"""
        try:
            result = Helper.is_webpage_with_content(url, timeout)
            return result["is_webpage"] and result["has_content"]
        except:
            return False
