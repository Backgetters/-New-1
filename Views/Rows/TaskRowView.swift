import SwiftUI

struct TaskRowView: View {
    let task: Task

    var body: some View {
        HStack {
            Text(task.title)
            Spacer()
            Image(systemName: "chevron.right")
                .foregroundColor(.secondary)
        }
        .contentShape(Rectangle())
    }
}

#Preview {
    TaskRowView(task: Task.sampleData.first!)
        .padding()
        .previewLayout(.sizeThatFits)
}