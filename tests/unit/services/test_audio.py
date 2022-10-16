import asyncio
from services.audio import get_audio, BaseAudio


async def test_join():
    audio: BaseAudio = get_audio()
    file = await audio.join_files(
        [
            "AwACAgIAAxkDAAIIJGGqi2wusiROsxHX4Dihw1STcYWKAALzFAACgHpRSSZWdzGLsZn2IgQ",
            "AwACAgIAAxkDAAIIJmGqi21T_3L65koWRUrsk9K4RLzgAAL1FAACgHpRSa1PlYxVxHXrIgQ",
            "AwACAgIAAxkBAAII6mHPDEQ8FDiaH4MOhaijcSxB7GzEAAKvEQACj7V4Spn_lwbRnV_BIwQ",
            "AwACAgIAAxkDAAIIJ2Gqi218TcJl77rRQwapvuYG8vjkAAL2FAACgHpRSTxFqPIvcY0ZIgQ",
            "AwACAgIAAxkBAAII7GHPDEsdIlllA5nwzzLygvSd_XfQAAKwEQACj7V4SkjIziQlTqQaIwQ",
            "AwACAgIAAxkDAAIIKGGqi208IjOyNlDIXM8pN-JXhCYtAAL3FAACgHpRSWuenY9DwH9VIgQ",
            "AwACAgIAAxkBAAII7mHPDE8qJgRlSKUSSSiy8hvFYGL7AAKyEQACj7V4SgLTEqqjumGQIwQ",
            "AwACAgIAAxkDAAIIJWGqi2xseCQ0jcRBGQRNlEM61UhQAAL0FAACgHpRSdV9ZZoOnnTGIgQ"
        ],
        "chat_id.ogg"
    )
