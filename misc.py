"""Misc contains help functions."""


def recv_end(conn, end):
    """Recieve with END token."""
    total_data = []
    data = ''
    while True:
        data = conn.recv(8192).decode()
        if end in data:
            total_data.append(data[:data.find(end)])
            break
        total_data.append(data)
        if len(total_data) > 1:
            # check if end_of_data was split
            last_pair = total_data[-2] + total_data[-1]
            if end in last_pair:
                total_data[-2] = last_pair[:last_pair.find(end)]
                total_data.pop()
                break
    return ''.join(total_data)
