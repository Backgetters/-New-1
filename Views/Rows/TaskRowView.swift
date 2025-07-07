import SwiftUI

struct TaskRowView: View {
    let task: Task
    let viewModel: TaskViewModel
    
    var body: some View {
        HStack {
            Button(action: {
                viewModel.toggleCompletion(for: task)
            }) {
                Image(systemName: task.isCompleted ? "checkmark.circle.fill" : "circle")
                    .foregroundColor(task.isCompleted ? .green : .gray)
            }
            
            VStack(alignment: .leading, spacing: 4) {
                Text(task.title)
                    .font(.headline)
                    .strikethrough(task.isCompleted)
                    .foregroundColor(task.isCompleted ? .secondary : .primary)
                
                Text(task.detail)
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .lineLimit(2)
            }
            
            Spacer()
        }
        .padding(.vertical, 2)
    }
}

#Preview {
    TaskRowView(task: Task.sampleData[0], viewModel: TaskViewModel())
}