🎨 Frontend Setup (Flutter)
This guide explains how to set up and run the Socratic Tutor frontend using Flutter.

1️⃣ System Requirements
macOS (Apple Silicon or Intel)

Homebrew installed

2️⃣ Install Tools
Flutter
Install Flutter using Homebrew:

Bash

brew install --cask flutter
Check your Flutter installation:

Bash

flutter doctor
Xcode (for iOS/macOS)
Install Xcode from the App Store or Apple Developer website.

Then, run these commands in your terminal:

Bash

sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -runFirstLaunch
Install CocoaPods for managing iOS dependencies:

Bash

sudo gem install cocoapods
Android Studio (for Android)
Install Android Studio from the official website.

In Android Studio, go to Preferences → Appearance & Behavior → System Settings → Android SDK.

Install the following components:

Android SDK Platform

SDK Tools

Command-line Tools

Accept the licenses:

Bash

flutter doctor --android-licenses
IDEs
Install either VS Code (with the Flutter and Dart extensions) or Android Studio.

3️⃣ Environment Configuration
Edit your ~/.zshrc file to add the necessary paths:

Bash

export PATH="$PATH:/opt/homebrew/bin"
export PATH="$PATH:/opt/homebrew/lib/ruby/gems/3.4.0/bin"
Reload the file to apply the changes:

Bash

source ~/.zshrc
4️⃣ Project Setup
Navigate to the project directory:

Bash

cd frontend
If you are starting a new project, run:

Bash

flutter create .
Modify Project Files
In your pubspec.yaml file, add the following dependency:

YAML

dependencies:
  http: ^1.1.0
Then, get the dependencies:

Bash

flutter pub get
lib/main.dart: Replace the content of this file with the provided chat UI code (see the repository for details).

5️⃣ Running the App
Web
Bash

flutter run -d chrome
iOS Simulator
Bash

open -a Simulator
flutter run -d ios
Android Emulator
List your available emulators:

Bash

flutter emulators
Launch a specific emulator and run the app:

Bash

flutter emulators --launch <emulator_id>
flutter run -d <emulator_id>
✅ Verification
flutter doctor passes with no issues.

The app loads the Socratic Tutor screen.

Input sends requests to the backend and displays the responses correctly.