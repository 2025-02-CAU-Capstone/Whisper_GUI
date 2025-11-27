## Whisper_GUI Repository

- This is a repository for Whisper_GUI, which is an EXE file that the companies/lecturers could upload their videos into a database in the server.
- This is to get ready for the P2L service; since the P2L service matches the lecture's timestamp and the question by the lecture's text, generating a text for each lecture is a crucial step.
- This EXE file's purpose is to get rid of the need of dictating manually by automatically generate the text for each lecture uploaded.
<br>

- In the release tab, there are two files uploaded. This is actually two separate volumes for a singular exe file, and they can be reassembled by following these steps:

***

How to Reassemble the Application (2-part 7-Zip archive)

The application is split into two parts because GitHub only allows files ≤ 2 GB.

Step 1 — Download both files

`whisper_gui.7z.001`

`whisper_gui.7z.002`

Make sure they are in the same folder.

Step 2 — Install 7-Zip (Windows)

Download from: https://www.7-zip.org/download.html

Or install via Winget:

`winget install 7zip.7zip`

Step 3 — Recombine the files
Option A — Using GUI (Windows)

Right-click `whisper_gui.7z.001`

Click 7-Zip → Extract Here

You will get:

`whisper_gui.exe`

Option B — Using command line (all platforms)
`7z x whisper_gui.7z.001`


This will automatically read .002 and extract the original .exe.

***

This project is developed by Guebeen Lee, Mingyu Lee, and Dongyun Ha, for Capstone Design (1) subject in School of Computer Science and Engineering, Chung-Ang University.
