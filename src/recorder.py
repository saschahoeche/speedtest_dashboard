import speedtest
import sys
import os
import sqlite3

class InternetSpeedTest:
	def __init__(self, db_path='speedtest_results.db', servers=[], threads=None):
		"""
		Initializes the InternetSpeedTest instance with a database path, list of servers, and number of threads.
		
		:param db_path: Path to the SQLite database file. Defaults to 'speedtest_results.db'.
		:param servers: List of server IDs to use for the speed test. An empty list selects the best server.
		:param threads: Number of threads to use for download and upload tests. None uses the default number.
		"""
		self.servers = servers
		self.threads = threads
		self.results = None
		self.db_path = db_path
		self.check_db_exists_and_initialize()

	def check_db_exists_and_initialize(self):
		"""
		Checks if the database file exists and initializes it by creating the necessary table if it doesn't exist.
		"""
		db_exists = os.path.exists(self.db_path)
		if not db_exists:
			print("Database does not exist. Creating new database and initializing tables.")
		else:
			print("Database exists. Connecting...")
		self.create_db_table()

	def create_db_connection(self):
		"""
		Creates and returns a connection to the SQLite database.
		
		:return: A connection object to the SQLite database.
		:raises sqlite3.Error: If there is an error connecting to the database.
		"""
		try:
			conn = sqlite3.connect(self.db_path)
			return conn
		except sqlite3.Error as e:
			print(f"Error connecting to database: {e}")
			sys.exit(1)

	def create_db_table(self):
		"""
		Creates the results table in the database if it does not already exist.
		"""
		create_table_sql = """
		CREATE TABLE IF NOT EXISTS results (
			id TEXT PRIMARY KEY,
			download_speed_mbps REAL,
			upload_speed_mbps REAL,
			ping INTEGER,
			server_name TEXT,
			server_country TEXT,
			server_sponsor TEXT,
			server_id TEXT,
			timestamp TEXT,
			bytes_sent INTEGER,
			bytes_received INTEGER
		);
		"""
		conn = self.create_db_connection()
		try:
			c = conn.cursor()
			c.execute(create_table_sql)
		except sqlite3.Error as e:
			print(f"Error creating table: {e}")
			sys.exit(1)
		finally:
			conn.close()

	def run_test(self):
		"""
		Performs the internet speed test and stores the results in the instance variable `results`.
		
		:raises speedtest.SpeedtestException: If there is an error performing the speed test.
		"""
		try:
			s = speedtest.Speedtest()
			s.get_servers(self.servers)
			s.get_best_server()
			s.download(threads=self.threads)
			s.upload(threads=self.threads)
			self.results = s.results.dict()
		except speedtest.SpeedtestException as e:
			print(f"Error performing speed test: {e}")
			sys.exit(1)

	def extract_results(self):
		"""
		Extracts and returns the relevant results from the speed test.
		
		:return: A dictionary containing the extracted results, or None if no results are available.
		"""
		if not self.results:
			print("No results to extract. Please run the test first.")
			return None

		return {
			"download_speed_mbps": round(self.results['download'] / 1e6, 2),
			"upload_speed_mbps": round(self.results['upload'] / 1e6, 2),
			"ping": self.results['ping'],
			"server_name": self.results['server']['name'],
			"server_country": self.results['server']['country'],
			"server_sponsor": self.results['server']['sponsor'],
			"server_id": self.results['server']['id'],
			"timestamp": self.results['timestamp'],
			"bytes_sent": self.results['bytes_sent'],
			"bytes_received": self.results['bytes_received']
		}

	def print_results(self):
		"""
		Prints the results of the internet speed test in a user-friendly format.
		"""
		if not self.results:
			print("No results available. Please run the test first.")
			return

		# Assuming extract_results method returns a dictionary of the relevant results
		extracted_results = self.extract_results()
		if extracted_results:
			print("Internet Speed Test Results:")
			print(f"Download Speed: {extracted_results['download_speed_mbps']} Mbps")
			print(f"Upload Speed: {extracted_results['upload_speed_mbps']} Mbps")
			print(f"Ping: {extracted_results['ping']} ms")
			print(f"Server Name: {extracted_results['server_name']}")
			print(f"Server Country: {extracted_results['server_country']}")
			print(f"Server Sponsor: {extracted_results['server_sponsor']}")
			print(f"Test Time: {extracted_results['timestamp']}")
		else:
			print("No results to display.")
	
    
			
    

# Example usage
if __name__ == "__main__":
    speed_test = InternetSpeedTest()
    speed_test.run_test()
    results = speed_test.extract_results()
    if results:
        speed_test.print_results()