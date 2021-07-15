from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base



class Client(Base):
    __tablename__ = 'client'
    client_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=False)
    # created_at = Column(DateTime, default=datetime.now)
    # updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # clusters = relationship("Cluster", back_populates='parent_client')


class ClusterType(Base):
    __tablename__ = 'cluester_type'
    cluster_type_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    # created_at = Column(DateTime, default=datetime.now)
    # updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Cluster(Base):
    __tablename__ = 'cluster'
    cluster_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    client_id = Column(Integer, ForeignKey("client.client_id"))
    cluster_state = Column(Integer)
    # created_at = Column(DateTime, default=datetime.now)
    # updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
#
#     test_suites = relationship("TestSuite", back_populates='parent_cluster')
#     parent_client = relationship("Client", back_populates='clusters')
#
#
# class TestSuite(Base):
#     __tablename__ = 'test_suite'
#     test_suite_id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     cluster_id = Column(Integer, ForeignKey("cluster.cluster_id"))
#     # created_at = Column(DateTime, default=datetime.now)
#     # updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
#
#     parent_cluster = relationship("Cluster", back_populates="test_suites")
#     test_cases = relationship("TestCase", back_populates="parent_suite")
#     tasks = relationship("Task", back_populates="task_suite")
#
#
# class TestCase(Base):
#     __tablename__ = 'test_case'
#     test_case_id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     description = Column(String, index=True)
#     test_suite_id = Column(Integer, ForeignKey("test_suite.test_suite_id"))
#     # created_at = Column(DateTime, default=datetime.now)
#     # updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
#
#     parent_suite = relationship("TestSuite", back_populates="test_cases")
#
