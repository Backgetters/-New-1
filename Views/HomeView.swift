import SwiftUI

struct HomeView: View {
    @EnvironmentObject private var viewModel: TaskViewModel

    var body: some View {
        List {
            ForEach(viewModel.tasks) { task in
                NavigationLink(value: task) {
                    TaskRowView(task: task)
                }
            }
            .onDelete(perform: viewModel.delete)
        }
        .navigationTitle("Tasks")
        .navigationDestination(for: Task.self) { task in
            DetailView(task: task)
        }
        .toolbar {
            ToolbarItem(placement: .navigationBarLeading) {
                NavigationLink {
                    SettingsView()
                } label: {
                    Image(systemName: "gear")
                }
            }
            ToolbarItem(placement: .navigationBarTrailing) {
                Button {
                    viewModel.addSample()
                } label: {
                    Image(systemName: "plus")
                }
            }
        }
    }
}

#Preview {
    NavigationStack {
        HomeView()
            .environmentObject(TaskViewModel())
    }
}