import XCTest
@testable import WeekendApp

final class WeekendAppTests: XCTestCase {
    
    func testTaskSampleDataCount() {
        // Test that sample data contains exactly 3 items
        XCTAssertEqual(Task.sampleData.count, 3, "Task sample data should contain exactly 3 items")
    }
    
    func testTaskViewModel() {
        let viewModel = TaskViewModel()
        
        // Test initial state
        XCTAssertEqual(viewModel.tasks.count, 3, "TaskViewModel should initialize with 3 sample tasks")
        
        // Test adding a sample task
        viewModel.addSample()
        XCTAssertEqual(viewModel.tasks.count, 4, "TaskViewModel should have 4 tasks after adding one")
        
        // Test deleting a task
        let indexSet = IndexSet(integer: 0)
        viewModel.deleteTask(at: indexSet)
        XCTAssertEqual(viewModel.tasks.count, 3, "TaskViewModel should have 3 tasks after deleting one")
    }
    
    func testTaskToggleCompletion() {
        let viewModel = TaskViewModel()
        let firstTask = viewModel.tasks.first!
        let initialCompletionState = firstTask.isCompleted
        
        viewModel.toggleCompletion(for: firstTask)
        
        let updatedTask = viewModel.tasks.first { $0.id == firstTask.id }!
        XCTAssertEqual(updatedTask.isCompleted, !initialCompletionState, "Task completion state should be toggled")
    }
}