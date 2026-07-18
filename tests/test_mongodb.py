import os
import sys
import traceback
from pymongo.database import Database
from pymongo.collection import Collection

# Adjust the path to make sure src is discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.mongodb import MongoDBManager

class TestRunner:
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0

    def run_test(self, name, test_func):
        self.total += 1
        print("-" * 50)
        print(f"Running {name}")
        print("-" * 50)
        try:
            test_func()
            print("\nPASS\n")
            self.passed += 1
        except AssertionError as e:
            print(f"\nFAIL: {e}\n")
            self.failed += 1
        except Exception as e:
            print(f"\nFAIL: Unexpected error: {traceback.format_exc()}\n")
            self.failed += 1


# Global manager to reuse for the tests
global_manager = MongoDBManager()


def test_mongodb_connection():
    db = global_manager.connect()
    assert db is not None, "Connect should return a database instance"
    assert isinstance(db, Database), "Returned object should be a Database"


def test_database_retrieval():
    db = global_manager.get_database()
    assert db is not None, "get_database should return database instance"
    assert db.name == "marketmind_ai", f"Expected db name 'marketmind_ai', got '{db.name}'"


def test_reports_collection_retrieval():
    coll = global_manager.get_collection("reports")
    assert coll is not None, "Collection should not be None"
    assert isinstance(coll, Collection), "Returned object should be a Collection"
    assert coll.name == "reports", f"Expected collection name 'reports', got '{coll.name}'"


def test_invalid_collection_name():
    try:
        global_manager.get_collection("")
        assert False, "Empty string should raise ValueError"
    except ValueError:
        pass
        
    try:
        global_manager.get_collection(None)
        assert False, "None should raise TypeError"
    except TypeError:
        pass


def test_invalid_collection_type():
    invalid_types = [123, [], {}]
    for inv in invalid_types:
        try:
            global_manager.get_collection(inv)
            assert False, f"{type(inv)} should raise TypeError"
        except TypeError:
            pass


def test_singleton_connection_reuse():
    mgr2 = MongoDBManager()
    assert id(global_manager) == id(mgr2), "MongoDBManager should be a singleton"
    assert global_manager._client is mgr2._client, "Should reuse the same MongoClient instance"


def test_ping_verification():
    result = global_manager._client.admin.command('ping')
    assert result.get('ok') == 1.0, "Ping should return ok: 1.0"


def test_connection_close():
    global_manager.close()
    assert global_manager._client is None, "Client should be None after close"
    assert global_manager._db is None, "DB should be None after close"


def test_missing_env_var_handling():
    old_instance = MongoDBManager._instance
    MongoDBManager._instance = None
    
    original_uri = os.environ.get("MONGODB_URI")
    # Setting to spaces bypasses dotenv overwriting while triggering validation error
    os.environ["MONGODB_URI"] = "   "
    
    try:
        try:
            MongoDBManager()
            assert False, "Should raise ValueError for missing MONGODB_URI"
        except ValueError as e:
            assert "MONGODB_URI" in str(e), "Exception message should mention MONGODB_URI"
    finally:
        MongoDBManager._instance = old_instance
        if original_uri is not None:
            os.environ["MONGODB_URI"] = original_uri
        else:
            del os.environ["MONGODB_URI"]


def test_connection_failure_handling():
    old_instance = MongoDBManager._instance
    MongoDBManager._instance = None
    
    original_uri = os.environ.get("MONGODB_URI")
    # Use a fast timeout to fail quickly
    os.environ["MONGODB_URI"] = "mongodb://invalid_user:invalid_pass@127.0.0.1:27017/?serverSelectionTimeoutMS=1000"
    
    try:
        temp_mgr = MongoDBManager()
        try:
            temp_mgr.connect()
            assert False, "Should raise ConnectionError for invalid connection"
        except ConnectionError:
            pass
        except Exception as e:
            assert type(e).__name__ == "ConnectionError", f"Expected ConnectionError, got {type(e).__name__}"
    finally:
        MongoDBManager._instance = old_instance
        if original_uri is not None:
            os.environ["MONGODB_URI"] = original_uri
        else:
            del os.environ["MONGODB_URI"]


if __name__ == "__main__":
    print("==================================================")
    print("Testing MongoDBManager")
    print("==================================================\n")

    runner = TestRunner()
    
    runner.run_test("MongoDB Connection Test", test_mongodb_connection)
    runner.run_test("Database Retrieval Test", test_database_retrieval)
    runner.run_test("Reports Collection Retrieval Test", test_reports_collection_retrieval)
    runner.run_test("Invalid Collection Name Test", test_invalid_collection_name)
    runner.run_test("Invalid Collection Type Test", test_invalid_collection_type)
    runner.run_test("Singleton Connection Reuse Test", test_singleton_connection_reuse)
    runner.run_test("Ping Verification Test", test_ping_verification)
    runner.run_test("Connection Close Test", test_connection_close)
    runner.run_test("Missing Environment Variable Handling Test", test_missing_env_var_handling)
    runner.run_test("Authentication / Connection Failure Handling Test", test_connection_failure_handling)

    print("==================================================")
    print("Test Summary")
    print("==================================================")
    print(f"Total Tests : {runner.total}")
    print(f"Passed      : {runner.passed}")
    print(f"Failed      : {runner.failed}")
    print("==================================================")

    if runner.failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)
