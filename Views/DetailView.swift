import SwiftUI

struct DetailView: View {
    let task: Task
    
    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            HStack {
                Image(systemName: task.isCompleted ? "checkmark.circle.fill" : "circle")
                    .foregroundColor(task.isCompleted ? .green : .gray)
                    .font(.title2)
                
                Text(task.title)
                    .font(.title)
                    .fontWeight(.bold)
                    .strikethrough(task.isCompleted)
                
                Spacer()
            }
            
            Text("Details")
                .font(.headline)
                .foregroundColor(.secondary)
            
            Text(task.detail)
                .font(.body)
                .lineSpacing(4)
            
            Spacer()
        }
        .padding()
        .navigationTitle("Task Details")
        .navigationBarTitleDisplayMode(.inline)
    }
}

#Preview {
    NavigationStack {
        DetailView(task: Task.sampleData[0])
    }
}