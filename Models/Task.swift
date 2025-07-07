import Foundation

struct Task: Identifiable, Codable, Hashable {
    let id: UUID
    var title: String
    var detail: String

    init(id: UUID = UUID(), title: String, detail: String) {
        self.id = id
        self.title = title
        self.detail = detail
    }
}

extension Task {
    /// Three example tasks to populate the UI while developing.
    static let sampleData: [Task] = [
        Task(title: "Buy groceries", detail: "Milk, Bread, Eggs"),
        Task(title: "Walk the dog", detail: "Take Fido to the park"),
        Task(title: "Read a book", detail: "Finish reading SwiftUI for Dummies")
    ]
}