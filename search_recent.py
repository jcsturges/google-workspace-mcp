#!/usr/bin/env python3
"""Search recent files in Google Drive"""

import sys
from datetime import datetime

from google_workspace_mcp.drive_client import DriveClient


def format_file_info(file):
    """Format file information for display"""
    name = file.get("name", "Unknown")
    file_id = file.get("id", "")
    mime_type = file.get("mimeType", "").split(".")[-1]
    modified = file.get("modifiedTime", "")
    size = file.get("size", "N/A")
    link = file.get("webViewLink", "")

    # Parse and format date
    if modified:
        dt = datetime.fromisoformat(modified.replace("Z", "+00:00"))
        modified = dt.strftime("%Y-%m-%d %H:%M")

    # Format size
    if size != "N/A":
        size_int = int(size)
        if size_int < 1024:
            size = f"{size_int} B"
        elif size_int < 1024 * 1024:
            size = f"{size_int / 1024:.1f} KB"
        else:
            size = f"{size_int / (1024 * 1024):.1f} MB"

    return {
        "name": name,
        "id": file_id,
        "type": mime_type,
        "modified": modified,
        "size": size,
        "link": link,
    }


def main():
    """Main function"""
    print("🔍 Google Drive 최근 문서 검색 중...")
    print()

    client = DriveClient()

    try:
        # Authenticate
        client.authenticate()
        print("✅ 인증 성공!\n")

        # Get recent files
        files = client.get_recent_files(max_results=20)

        if not files:
            print("📭 최근 문서가 없습니다.")
            return

        print(f"📄 최근 문서 {len(files)}개:\n")
        print("-" * 80)

        for idx, file in enumerate(files, 1):
            info = format_file_info(file)
            print(f"{idx}. {info['name']}")
            print(f"   📅 수정: {info['modified']}")
            print(f"   📦 크기: {info['size']}")
            print(f"   🔗 링크: {info['link']}")
            print(f"   🆔 ID: {info['id']}")
            print()

    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
