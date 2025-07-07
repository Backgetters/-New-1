# WeekendApp

A simple iOS 17 SwiftUI task management app that can be built in a weekend.

## Features

- **Login Screen**: Email and password validation with form validation
- **Task List**: View and manage your tasks with completion tracking
- **Task Details**: Detailed view for each task
- **Settings**: Dark mode and notifications preferences
- **Add Tasks**: Quickly add sample tasks
- **Delete Tasks**: Swipe to delete tasks from the list

## Project Structure

```
WeekendApp/
├── WeekendAppApp.swift              # Main app entry point
├── Models/
│   └── Task.swift                   # Task data model with sample data
├── ViewModels/
│   └── TaskViewModel.swift          # MVVM state management
├── Views/
│   ├── LoginView.swift              # Login screen with validation
│   ├── HomeView.swift               # Main task list view
│   ├── Rows/
│   │   └── TaskRowView.swift        # Individual task row UI
│   ├── DetailView.swift             # Task detail view
│   └── SettingsView.swift           # Settings with toggles
├── Tests/
│   └── WeekendAppTests.swift        # Unit tests
└── README.md                        # This file
```

## Build Instructions

### Prerequisites
- Xcode 15 or later
- iOS 17 SDK
- iPhone 15 Simulator (or any iOS 17+ device)

### Building the Project

1. **Open in Xcode**:
   - Open Xcode
   - Select "Open a project or file"
   - Navigate to the WeekendApp folder
   - Select the `.xcodeproj` file (you may need to create this first)

2. **Create Xcode Project** (if needed):
   - In Xcode, select "File" → "New" → "Project"
   - Choose "iOS" → "App"
   - Product Name: `WeekendApp`
   - Interface: SwiftUI
   - Language: Swift
   - Replace the generated files with the files from this project

3. **Build the Project**:
   - Press `⌘B` to build the project
   - Ensure all files compile without errors

4. **Run the App**:
   - Select iPhone 15 Simulator
   - Press `⌘R` to run the app

### Testing

- Press `⌘U` to run unit tests
- Tests verify sample data count and ViewModel functionality

## Usage

1. **Login**: Enter any email and password (validation requires both fields to be non-empty)
2. **Home Screen**: View your tasks, tap to see details
3. **Add Tasks**: Tap the "+" button to add sample tasks
4. **Complete Tasks**: Tap the circle icon to mark tasks as complete
5. **Settings**: Tap the gear icon to access dark mode and notification preferences
6. **Delete Tasks**: Swipe left on any task to delete it

## Technical Details

- **iOS Target**: iOS 17+
- **Architecture**: MVVM (Model-View-ViewModel)
- **UI Framework**: SwiftUI
- **Navigation**: NavigationStack (iOS 16+)
- **Data Persistence**: @AppStorage for settings
- **Testing**: XCTest framework

## SwiftUI Features Used

- NavigationStack for navigation
- @StateObject and @Published for reactive state management
- @AppStorage for persistent settings
- Form and List views
- Toolbar and navigation customization
- Sheet presentation for settings
- #Preview for SwiftUI previews

## Notes

- This is a demo app with sample data
- No network connectivity or real authentication
- Settings are stored locally using @AppStorage
- Designed to be completed in a weekend by a beginner
