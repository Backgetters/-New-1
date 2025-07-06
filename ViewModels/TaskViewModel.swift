import SwiftUI

@MainActor
final class TaskViewModel: ObservableObject {
    @Published var tasks: [Task] = Task.sampleData

    /// Adds a placeholder task so non-coders can quickly see something happen.
    func addSample() {
        let newTask = Task(title: "New Task", detail: "Describe something to do…")
        tasks.append(newTask)
    }

    /// Removes tasks using the standard swipe-to-delete gesture.
    func delete(at offsets: IndexSet) {
        tasks.remove(atOffsets: offsets)
    }
}