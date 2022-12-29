import requests
import pandas as pd
import time

headers = {
    'authority': 'www.lazada.co.id',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'cookie': 'lzd_cid=aef387c0-9dca-4adf-8ed8-7d9749575768; t_uid=aef387c0-9dca-4adf-8ed8-7d9749575768; '
              'hng=ID|id|IDR|360; userLanguageML=id; lzd_sid=17361b11e6ba4c08bf34e4ec16dd57fe; _m_h5_tk=d3a8d720e42080c27c659984e086c2db_1672229358793; _m_h5_tk_enc=67c9aebb52d9189dcc57cddd664cb06a; _tb_token_=feee71575be73; _bl_uid=8bln7cvs70dhs39gt6pL9sh6s0IU; t_fv=1672221079355; t_sid=lXeSG3BBGohcUYgT6RmdtUSbIHr0YaWt; utm_channel=NA; cna=j7ezGSXYITwCAcpDKPa5rFWw; tfstk=ch2fBeO5sEYbgr5w3osP0dv7PXk1ZTQSqsgYcZCAVPuJN2qfi99ERAXUsUDZX01..; l=eBTaDESeTnxku71MBOfZnurza77TsIRAguPzaNbMiOCP_J5p5bKhW6SdRVY9CnMNhswHR3ykA-nXBeYBqIDjLbHEAjH5SZkmn; isg=BBoasHxALblRiaEVRbarUS7Ba8A8S54lOnUtxySTz614l7rRDNlKNNHhZ3sLRxa9',
    'referer': 'https://www.lazada.co.id/catalog/?q=baju+wanita&_keyori=ss&from=input&spm=a2o4j.home.search.go'
               '.579953e09zLBOW',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 '
                  'Safari/537.36',
    'x-csrf-token': 'feee71575be73',
    'x-requested-with': 'XMLHttpRequest',
    'x-umidtoken': 'T2gADCZKWDu6YR12UY_C_YaBf7tCwce6oZT8zGjPZm8_GjNYjvuvoYD6UT9UvQn7Plw='
}


def dataframe(data):
    return pd.DataFrame(data, columns=['Product Name', 'Price'])


def save_csv(df):
    df.to_csv('baju-lazada.csv', index=False)
    print('Data saved to local disk')


def merge_sort(arr):
    if len(arr) > 1:
        # Split the array into two halves
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        # Recursively sort the two halves
        merge_sort(left_half)
        merge_sort(right_half)

        # Merge the sorted halves
        i = 0  # Index for left half
        j = 0  # Index for right half
        k = 0  # Index for merged array
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Copy remaining elements, if any
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1


if __name__ == '__main__':
    products = []
    price_list = []

    print('Start scraping data...')
    for i in range(1, 101):
        url = 'https://www.lazada.co.id/catalog/?_keyori=ss&ajax=true&from=search_history&isFirstRequest=true&page={}' \
              '&q=baju%20wanita&spm=a2o4j.home.search.1.579953e0i88ITF&sugg=baju%20wanita_0_1'.format(i)

        qsp = {
            '_keyori': 'ss',
            'ajax': 'true',
            'from': 'input',
            'isFirstRequest': 'true',
            'page': i,
            'q': 'baju wanita',
            'spm': 'a2o4j.home.search.1.579953e0i88ITF'
        }

        res = requests.request("GET", url, headers=headers, params=qsp).json()
        rows = res['mods']['listItems']

        for j in range(0, len(rows)):
            product_name = res['mods']['listItems'][j]['name']
            remove_rp = res['mods']['listItems'][j]['priceShow'].replace('Rp', '')
            res_price = remove_rp.replace('.', '')
            product_price = int(res_price)
            products.append(
                (product_name, product_price)
            )
            price_list.append(product_price)
    print('Scraping data selesai!')

    # save data ke file csv
    data = dataframe(products)
    save_csv(data)

    method_msg = "Enter sorting method:\n1. Selection Sort \
            \n2. Merge Sort\n3. Exit \nEnter your choice: "
    method = input(method_msg)

    if method == '1':
        ss_time = time.time()
        iteration = 0

        print('data sebelum sorting : ', price_list)
        for i in range(len(price_list)):
            # Cari  minimum elemen
            min_idx = i
            for j in range(i + 1, len(price_list)):
                if price_list[min_idx] > price_list[j]:
                    min_idx = j
            # Tukar elemen minimum yang ditemukan dengan elemen yang pertama
            price_list[i], price_list[min_idx] = price_list[min_idx], price_list[i]

            it_time = time.time()
            iteration = i

            if iteration == 500:
                print(f'\nData ke : {iteration}\twaktu sorting : {(it_time - ss_time)} seconds')
            elif iteration == 1000:
                print(f'Data ke : {iteration}\twaktu sorting : {(it_time - ss_time)} seconds')
            elif iteration == 1500:
                print(f'Data ke : {iteration}\twaktu sorting : {(it_time - ss_time)} seconds')
            elif iteration == 2000:
                print(f'Data ke : {iteration}\twaktu sorting : {(it_time - ss_time)} seconds')
            elif iteration == 2500:
                print(f'Data ke : {iteration}\twaktu sorting : {(it_time - ss_time)} seconds')
            elif iteration == 3000:
                print(f'Data ke : {iteration}\twaktu sorting : {(it_time - ss_time)} seconds')
            elif iteration == 3500:
                print(f'Data ke : {iteration}\twaktu sorting : {(it_time - ss_time)} seconds')

        es_time = time.time()
        fb_time = es_time - ss_time
        print('Total waktu sorting data : ', fb_time, 'seconds\n')
        print('data sesudah sorting : ', price_list)
    elif method == '2':
        print("Data sebelum sorting:", price_list)

        # Measure time before sorting
        start_time = time.time()

        # Sort the array
        merge_sort(price_list)

        # Print running time for every 10th iteration
        for i, item in enumerate(price_list):
            if i % 500 == 0:
                end_time = time.time()
                print(f"Data ke : {i}: {end_time - start_time} seconds")

        # Measure time after sorting
        end_time = time.time()

        # Calculate elapsed time
        elapsed_time = end_time - start_time
        print("Elapsed time:", elapsed_time)

        # Print sorted array
        print("Sorted array:", price_list)
    elif method == '3':
        print('Program selesai!\n')
        exit()
    else:
        print('\ninput tidak sesuai\n')
