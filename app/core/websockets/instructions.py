from enum import Enum

class InstructionType(Enum):
    GET_PRINTER_LIST = "get_printer_list"
    GET_PRINTER_STATUS = "get_printer_status"
    SUBMIT_PRINT_JOB = "submit_print_job"
    GET_PRINT_JOB_STATUS = "get_print_job_status"
    CANCEL_PRINT_JOB = "cancel_print_job"

class Instruction:
    def __init__(self, type: InstructionType, payload: dict = None):
        self.type = type
        self.payload = payload or {}

    def to_dict(self):
        return {
            "type": self.type.value,
            "payload": self.payload
        }

# Example instructions
GET_PRINTER_LIST = Instruction(InstructionType.GET_PRINTER_LIST)
GET_PRINTER_STATUS = Instruction(InstructionType.GET_PRINTER_STATUS, {"printer_id": "printer1"})
SUBMIT_PRINT_JOB = Instruction(InstructionType.SUBMIT_PRINT_JOB, {"printer_id": "printer1", "document_url": "https://example.com/document.pdf"})
GET_PRINT_JOB_STATUS = Instruction(InstructionType.GET_PRINT_JOB_STATUS, {"job_id": "job1"})
CANCEL_PRINT_JOB = Instruction(InstructionType.CANCEL_PRINT_JOB, {"job_id": "job1"})