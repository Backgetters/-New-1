import SwiftUI

struct DetailView: View {
    let task: Task

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Text(task.title)
                    .font(.title)
                    .bold()
                Text(task.detail)
                    .font(.body)
                Spacer()
            }
            .padding()
        }
        .navigationTitle("Detail")
    }
}

#Preview {
    NavigationStack {
        DetailView(task: Task.sampleData[0])
    }
}