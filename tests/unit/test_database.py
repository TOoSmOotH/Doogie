import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.database import Base, User, UserRole, UserStatus


# Create a test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """Create a clean database session for a test."""
    # Create the tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        
    # Drop the tables after the test
    Base.metadata.drop_all(bind=engine)


def test_create_user(db_session):
    """Test creating a user in the database."""
    # Create a user
    user = User(
        email="test@example.com",
        hashed_password="hashed_password",
        full_name="Test User",
        role=UserRole.USER,
        status=UserStatus.ACTIVE,
    )
    
    # Add the user to the database
    db_session.add(user)
    db_session.commit()
    
    # Query the user
    db_user = db_session.query(User).filter(User.email == "test@example.com").first()
    
    # Check that the user was created correctly
    assert db_user is not None
    assert db_user.email == "test@example.com"
    assert db_user.full_name == "Test User"
    assert db_user.role == UserRole.USER
    assert db_user.status == UserStatus.ACTIVE


def test_user_role_enum(db_session):
    """Test the UserRole enum."""
    # Create users with different roles
    admin_user = User(
        email="admin@example.com",
        hashed_password="hashed_password",
        full_name="Admin User",
        role=UserRole.ADMIN,
        status=UserStatus.ACTIVE,
    )
    
    regular_user = User(
        email="user@example.com",
        hashed_password="hashed_password",
        full_name="Regular User",
        role=UserRole.USER,
        status=UserStatus.ACTIVE,
    )
    
    # Add the users to the database
    db_session.add(admin_user)
    db_session.add(regular_user)
    db_session.commit()
    
    # Query the users
    db_admin = db_session.query(User).filter(User.email == "admin@example.com").first()
    db_user = db_session.query(User).filter(User.email == "user@example.com").first()
    
    # Check that the roles were set correctly
    assert db_admin.role == UserRole.ADMIN
    assert db_user.role == UserRole.USER
    
    # Check string representation
    assert db_admin.role.value == "admin"
    assert db_user.role.value == "user"


def test_user_status_enum(db_session):
    """Test the UserStatus enum."""
    # Create users with different statuses
    active_user = User(
        email="active@example.com",
        hashed_password="hashed_password",
        full_name="Active User",
        role=UserRole.USER,
        status=UserStatus.ACTIVE,
    )
    
    pending_user = User(
        email="pending@example.com",
        hashed_password="hashed_password",
        full_name="Pending User",
        role=UserRole.USER,
        status=UserStatus.PENDING,
    )
    
    inactive_user = User(
        email="inactive@example.com",
        hashed_password="hashed_password",
        full_name="Inactive User",
        role=UserRole.USER,
        status=UserStatus.INACTIVE,
    )
    
    # Add the users to the database
    db_session.add(active_user)
    db_session.add(pending_user)
    db_session.add(inactive_user)
    db_session.commit()
    
    # Query the users
    db_active = db_session.query(User).filter(User.email == "active@example.com").first()
    db_pending = db_session.query(User).filter(User.email == "pending@example.com").first()
    db_inactive = db_session.query(User).filter(User.email == "inactive@example.com").first()
    
    # Check that the statuses were set correctly
    assert db_active.status == UserStatus.ACTIVE
    assert db_pending.status == UserStatus.PENDING
    assert db_inactive.status == UserStatus.INACTIVE
    
    # Check string representation
    assert db_active.status.value == "active"
    assert db_pending.status.value == "pending"
    assert db_inactive.status.value == "inactive"