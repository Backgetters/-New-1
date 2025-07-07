import SwiftUI

class TaskViewModel: ObservableObject {
    @Published var tasks: [Task] = Task.sampleData
    
    func addSample() {
        let newTask = Task(title: "New Task", detail: "This is a new sample task", isCompleted: false)
        tasks.append(newTask)
    }
    
    func deleteTask(at indexSet: IndexSet) {
        tasks.remove(atOffsets: indexSet)
    }
    
    func toggleCompletion(for task: Task) {
        if let index = tasks.firstIndex(where: { $0.id == task.id }) {
            tasks[index].isCompleted.toggle()
        }
    }
}