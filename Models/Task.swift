import Foundation

struct Task: Identifiable, Codable {
    let id = UUID()
    var title: String
    var detail: String
    var isCompleted: Bool = false
    
    static let sampleData: [Task] = [
        Task(title: "Learn SwiftUI", detail: "Complete the SwiftUI tutorial and build a simple app", isCompleted: false),
        Task(title: "Go for a walk", detail: "Take a 30-minute walk in the park to get some fresh air", isCompleted: true),
        Task(title: "Read a book", detail: "Finish reading the current chapter of my favorite novel", isCompleted: false)
    ]
}