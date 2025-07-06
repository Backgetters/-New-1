import SwiftUI

struct SettingsView: View {
    @AppStorage("isDarkMode") private var isDarkMode = false
    @AppStorage("isNotificationsOn") private var isNotificationsOn = false

    var body: some View {
        Form {
            Toggle("Dark Mode", isOn: $isDarkMode)
            Toggle("Notifications", isOn: $isNotificationsOn)
        }
        .navigationTitle("Settings")
    }
}

#Preview {
    NavigationStack {
        SettingsView()
    }
}