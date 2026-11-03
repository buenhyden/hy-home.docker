"""Explicit opt-in native P03 model rehearsals; never part of default execution."""

import os
import unittest

from tests.validation._p03_notebook_native import (
    DockerNotebookRuntime,
    NotebookNativeLifecycle,
)
from tests.validation._p03_worker_model_native import WorkerModelNativeRehearsal


@unittest.skipUnless(
    os.environ.get("P03_NOTEBOOK_NATIVE_REHEARSAL") == "1",
    "exact isolated Notebook native opt-in required",
)
class NotebookModelsNativeExecutionTests(unittest.TestCase):
    def test_owned_notebook_model_data_restart_and_restore(self):
        receipt = NotebookNativeLifecycle(DockerNotebookRuntime()).run()
        self.assertEqual(receipt["native"], "PASS")
        self.assertEqual(receipt["embedding_dimensions"], 768)
        self.assertEqual(receipt["restore_matches_source"], True)
        self.assertEqual(receipt["cleanup"], "PASS")


@unittest.skipUnless(
    os.environ.get("P03_WORKER_MODEL_NATIVE_REHEARSAL") == "1",
    "exact isolated n8n Worker model native opt-in required",
)
class WorkerModelQueueNativeTests(unittest.TestCase):
    def test_main_dispatches_persisted_execution_to_worker_loopback_ollama(self):
        receipt = WorkerModelNativeRehearsal().run()
        self.assertEqual(receipt["native"], "PASS")
        self.assertEqual(receipt["queue_execution"], "PASS")
        self.assertEqual(receipt["worker_actor"], "PASS")
        self.assertEqual(receipt["model"], "gemma4:e2b")
        self.assertEqual(receipt["live_model_inference_claimed"], False)
        self.assertEqual(receipt["cleanup"], "PASS")
