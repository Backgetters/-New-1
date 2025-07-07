import XCTest
@testable import WeekendApp

final class WeekendAppTests: XCTestCase {
    func testSampleDataCount() {
        XCTAssertEqual(Task.sampleData.count, 3, "There should be exactly three sample tasks.")
    }
}