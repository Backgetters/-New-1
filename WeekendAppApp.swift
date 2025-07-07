import SwiftUI

@main
struct WeekendAppApp: App {
    @StateObject private var viewModel = TaskViewModel()
    @AppStorage("isDarkMode") private var isDarkMode = false
    var body: some Scene {
        WindowGroup {
            LoginView()
                .environmentObject(viewModel)
                .preferredColorScheme(isDarkMode ? .dark : .light)
        }
    }
}

#Preview {
    WeekendAppApp_Preview()
}

private struct WeekendAppApp_Preview: View {
    var body: some View {
        WeekendAppApp()
    }
}