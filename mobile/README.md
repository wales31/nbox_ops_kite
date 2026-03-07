# Mobile Prototype

The Android client is a Kotlin + Jetpack Compose prototype for the OpsPulse gateway.

## Features

- Dashboard tab for CPU, memory, disk, uptime, battery, and network
- Processes tab for top process inspection
- Alerts tab for mobile triage
- Setup tab to point the app at your laptop's gateway URL

## Build Notes

This environment does not include Gradle, so the Android project files were scaffolded but not built here. Open `mobile/` in Android Studio and let the IDE sync dependencies.

For an emulator on the same machine use:

```text
http://10.0.2.2:8090/
```

For a real phone on the same Wi-Fi use your laptop IP:

```text
http://192.168.x.x:8090/
```
