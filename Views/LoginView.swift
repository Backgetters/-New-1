import SwiftUI

struct LoginView: View {
    @EnvironmentObject private var viewModel: TaskViewModel
    @State private var email = ""
    @State private var password = ""
    @State private var isActive = false

    var body: some View {
        NavigationStack {
            VStack(spacing: 24) {
                Group {
                    TextField("Email", text: $email)
                        .textFieldStyle(.roundedBorder)
                        .keyboardType(.emailAddress)
                        .textInputAutocapitalization(.never)
                        .autocorrectionDisabled()

                    SecureField("Password", text: $password)
                        .textFieldStyle(.roundedBorder)
                }
                .textContentType(.oneTimeCode)

                Button("Login") {
                    isActive = true
                }
                .buttonStyle(.borderedProminent)
                .disabled(email.isEmpty || password.isEmpty)

                // Invisible NavigationLink that becomes active when the button is tapped.
                NavigationLink(destination: HomeView()
                                .environmentObject(viewModel),
                               isActive: $isActive) {
                    EmptyView()
                }
            }
            .padding()
            .navigationTitle("Login")
        }
    }
}

#Preview {
    LoginView()
        .environmentObject(TaskViewModel())
}