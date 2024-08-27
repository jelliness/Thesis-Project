import pandas as pd

class DataLoader:
    def __init__(self, file_path):
        """Initialize the DataLoader with a path to the CSV file."""
        self.file_path = file_path
        self.df = None

    def connect(self):
        """Simulate a database connection by loading the CSV data."""
        self.df = pd.read_csv(self.file_path)
    
    def get_all_data(self):
        """Return the entire DataFrame."""
        return self.df
    
    def get_unique_values(self, column_name):
        """Get unique values from a specific column."""
        if self.df is not None:
            return self.df[column_name].unique()
        else:
            raise ValueError("Data not loaded. Please call 'connect()' first.")
    
    def filter_data(self, column_name, value):
        """Filter the data based on a specific column and value."""
        if self.df is not None:
            return self.df[self.df[column_name] == value]
        else:
            raise ValueError("Data not loaded. Please call 'connect()' first.")
    
    def get_min_value(self, column_name):
        """Get the minimum value of a specific column."""
        if self.df is not None:
            return self.df[column_name].min()
        else:
            raise ValueError("Data not loaded. Please call 'connect()' first.")
    
    def get_max_value(self, column_name):
        """Get the maximum value of a specific column."""
        if self.df is not None:
            return self.df[column_name].max()
        else:
            raise ValueError("Data not loaded. Please call 'connect()' first.")
    
    def get_filtered_data(self, selected_colleges, selected_status, selected_years):
        """Filter the DataFrame based on multiple criteria."""
        if self.df is not None:
            filtered_df = self.df[
                (self.df['College'].isin(selected_colleges)) & 
                (self.df['PUBLISHED'].isin(selected_status)) & 
                (self.df['Year'].between(selected_years[0], selected_years[1]))
            ]
            return filtered_df
        else:
            raise ValueError("Data not loaded. Please call 'connect()' first.")
