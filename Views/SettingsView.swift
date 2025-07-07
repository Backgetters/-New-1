import SwiftUI

struct SettingsView: View {
    @AppStorage("darkMode") private var darkMode = false
    @AppStorage("notifications") private var notifications = true
    @Environment(\.dismiss) private var dismiss
    
    var body: some View {
        NavigationStack {
            Form {
                Section(header: Text("Preferences")) {
                    Toggle("Dark Mode", isOn: $darkMode)
                        .toggleStyle(SwitchToggleStyle())
                    
                    Toggle("Notifications", isOn: $notifications)
                        .toggleStyle(SwitchToggleStyle())
                }
                
                Section(header: Text("About")) {
                    HStack {
                        Text("Version")
                        Spacer()
                        Text("1.0.0")
                            .foregroundColor(.secondary)
                    }
                }
            }
            .navigationTitle("Settings")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
        }
        .preferredColorScheme(darkMode ? .dark : .light)
    }
}

#Preview {
    SettingsView()
}