import SwiftUI

struct HomeView: View {
    @StateObject private var viewModel = TaskViewModel()
    @State private var showingSettings = false
    
    var body: some View {
        NavigationStack {
            List {
                ForEach(viewModel.tasks) { task in
                    NavigationLink(destination: DetailView(task: task)) {
                        TaskRowView(task: task, viewModel: viewModel)
                    }
                }
                .onDelete(perform: viewModel.deleteTask)
            }
            .navigationTitle("My Tasks")
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button(action: {
                        showingSettings = true
                    }) {
                        Image(systemName: "gear")
                    }
                }
                
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: {
                        viewModel.addSample()
                    }) {
                        Image(systemName: "plus")
                    }
                }
            }
            .sheet(isPresented: $showingSettings) {
                SettingsView()
            }
        }
    }
}

#Preview {
    HomeView()
}