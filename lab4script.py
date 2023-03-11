from log_analysis import get_log_file_path_from_cmd_line, filter_log_by_regex
import pandas as pd 
import re
import os
import csv
def main():
    log_file = get_log_file_path_from_cmd_line(1)
    #records = filter_log_by_regex(log_file, 'SRC=(.*?) DST=(.*?) LEN=(.*?)', print_summary=True, print_records=True)
    dpt_tally = tally_port_traffic(log_file)
    for dpt, count in dpt_tally.items():
        if count> 100:
            generate_port_traffic_report(log_file, dpt)


    pass



# TODO: Step 8
def tally_port_traffic(log_file):
    dest_port_logs = filter_log_by_regex(log_file, 'DPT=(.+?)')[1]
    dpt_tally = {}
    for dpt_tuple in dest_port_logs:
        dpt_num = dpt_tuple[0]
        dpt_tally[dpt_num] = dpt_tally.get(dpt_num, 0) +1
    return dpt_tally

# TODO: Step 9
def generate_port_traffic_report(log_file, port_number):
     regex = r"^(.{6}) (.{8}).*SRC=(.+?) DST=(.+) .*spt=(.+?) " + f"DPT=({port_number}) "
     captured_data = filter_log_by_regex(log_file, regex)[1]
     report_df = pd.DataFrame(captured_data)
     report_header = ('Date', 'Time', 'Source IP Address', 'Destination IP Address', 'Source Port', 'Destination Port')
     report_df.to_csv(f'destination_port_{port_number}_report.csv', index=False, header=report_header)
    

# TODO: Step 11
def generate_invalid_user_report(log_file):
    regex = r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}).*Invalid user (\w+).*from ([\d\.]+)'
    report_header = ('Date', 'Time', 'Username', 'IP Address')
    with open(log_file, 'r') as log_file:
        lines = log_file.readlines()

    # Extract the relevant information
    invalid_user_data = []
    for line in lines:
        match = re.match(regex, line)
        if match:
            date_time = match.group(1)
            username = match.group(2)
            ip_address = match.group(3)
            month, date, time = date_time.split(' ', 2)
            invalid_user_data.append(
                {'date': month + ' ' + date, 'time': time, 'username': username, 'ip_address': ip_address})

    # Save the data as a CSV file
    output = os.path.join(os.path.dirname(log_file), 'invalid_users.csv')
    match.to_csv(f'{log_file}invalid_users.csv', header=report_header)
    with open(output, 'r', newline='') as file:

      return invalid_user_data

# TODO: Step 12
def generate_source_ip_log(log_file, ip_address):
    with open(log_file, 'r') as file:
     regex = r'\bSRC={}\b'.format(re.escape(ip_address))
    for line in file: 
     match = re.search(regex, line)
    if match: 
     report_df = pd.DataFrame(regex)
     output = 'source_ip_{}.log'.format(ip_address.replace('.', '_'))
     report_df = os.path.join(os.path.dirname(log_file), output)
     report_df.to_csv(output, header=None, index=None, sep=' ', mode='a', quoting=csv.QUOTE_NONE, quotechar="",
              escapechar=" ")
    return

if __name__ == '__main__':
    main()

