import models.printer as PrinterModel

class PrinterService:
    @staticmethod
    async def list_printers():
        """
        Lists all available printers.
        
        Returns:
            A list of printer details.
        """        
        pass

    @staticmethod
    async def get_printer_details(printer_id: str) -> PrinterModel:
        """
        Gets the details of a printer.
        
        Args:
            printer_id (str): The ID of the printer to get details for.
        
        Returns:
            PrinterModel: The details of the printer.
        """
        pass