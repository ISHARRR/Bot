
def trading_bot_crossover(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    running_msg(stock_symbol)

    cross = oanda.Oanda('101-004-14591208-007', oanda_stock_symbol, one_pip, 1)

    buy_id = 0
    sell_id = 0

    while True:
        try:
            current_sma200 = ema_sma.sma_200(stock_symbol, api_key)
            current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.ema_10_30(stock_symbol, api_key)

            email_message = 'Crossover Strategy'

            if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow)): # BUY
                trade_msg(stock_symbol, 'BUY')
                # email('BUY', stock_symbol, email_message)
                email('BUY - test', stock_symbol, email_message, 'private')
                if sell_id != 0:
                    cross.close_order(sell_id)
                    print('Trade ID:', sell_id, 'Status: CLOSED' + '\n')
                    email('Order Closed - test', str(sell_id), 'Check if order has been closed', 'private')
                    sell_id = 0
                buy_id = cross.create_order('CROSS', 'BUY')
                print('buy ID out: ', buy_id)

                while True:
                    time.sleep(60)
                    try:
                        current_sma200 = ema_sma.sma_200(stock_symbol, api_key)
                        current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.ema_10_30(stock_symbol, api_key)

                        if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow)): # SELL
                            if buy_id != 0:
                                cross.close_order(buy_id)
                                print('Trade ID:', buy_id, 'Status: CLOSED' + '\n')
                                email('Order Closed - test', str(buy_id), 'Check if order has been closed', 'private')
                                buy_id = 0
                        # if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_ema_slow > current_sma200)): # SELL
                            trade_msg(stock_symbol, 'SELL')
                            # email('SELL', stock_symbol, email_message)
                            email('SELL - test', stock_symbol, email_message, 'private')
                            sell_id = cross.create_order('CROSS', 'SELL')
                            break
                        # elif ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_ema_slow < current_sma200)): # breakout
                        #     break

                    except Exception as e :
                        exception_alert(e)
                        email('TEST BOT: EXCEPTION ERROR -', 'INNER LOOP', (str(traceback.format_exc()) + '\n' + str(e)), 'private')
                        time.sleep(random.randint(60, 150))

                    time.sleep(540)

            if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow)): # SELL
                trade_msg(stock_symbol, 'SELL')
                # email('SELL', stock_symbol, email_message)
                email('SELL - test', stock_symbol, email_message, 'private')
                if buy_id != 0:
                    cross.close_order(buy_id)
                    print('Trade ID:', buy_id, 'Status: CLOSED' + '\n')
                    email('Order Closed - test', str(buy_id), 'Check if order has been closed', 'private')
                    buy_id = 0
                sell_id = cross.create_order('CROSS', 'SELL')

                while True:
                    time.sleep(60)
                    try:
                        current_sma200 = ema_sma.sma_200(stock_symbol, api_key)
                        current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.ema_10_30(stock_symbol, api_key)

                        if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow)):  # BUY
                            if sell_id != 0:
                                cross.close_order(sell_id)
                                print('Trade ID:', sell_id, 'Status: CLOSED' + '\n')
                                email('Order Closed - test', str(sell_id), 'Check if order has been closed', 'private')
                                sell_id = 0
                        # if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_ema_slow < current_sma200)):  # BUY
                            trade_msg(stock_symbol, 'BUY')
                            # email('BUY', stock_symbol, email_message)
                            email('BUY - test', stock_symbol, email_message, 'private')
                            buy_id = cross.create_order('CROSS', 'BUY')
                            break
                        # elif ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_ema_slow > current_sma200)): # breakout
                        #     break

                    except Exception as e :
                        exception_alert(e)
                        email('TEST BOT: EXCEPTION ERROR -', 'INNER LOOP', (str(traceback.format_exc()) + '\n' + str(e)), 'private')
                        time.sleep(random.randint(60, 150))

                    time.sleep(540)

        except Exception as e :
            exception_alert(e)
            email('TEST BOT: EXCEPTION', 'ERROR', (str(traceback.format_exc()) + '\n' + str(e)), 'private')
            time.sleep(random.randint(60, 150))

        time.sleep(600)



def sma_crossover_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    running_msg(stock_symbol)

    account = '101-004-14591208-006'

    cross = oanda.Oanda(account, oanda_stock_symbol, one_pip, 1)

    buy_id = 0
    sell_id = 0
    while True:
        try:
            current_sma200 = ema_sma.sma_200(stock_symbol, api_key)
            current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.ema_10_30(stock_symbol, api_key)

            email_message = 'Crossover Strategy'

            if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_ema_slow < current_sma200)): # BUY

                trade_msg(stock_symbol, 'BUY')
                # email('BUY', stock_symbol, email_message)
                email('BUY - test', stock_symbol, email_message, 'private')
                if sell_id != 0:
                    cross.close_order(sell_id)
                    print('Trade ID:', sell_id, 'Status: CLOSED' + '\n')
                    email('Order Closed - test', str(sell_id), 'Check if order has been closed', 'private')
                    sell_id = 0
                buy_id = cross.create_order('CROSS', 'BUY')

                while True:
                    time.sleep(60)
                    try:
                        current_sma200 = ema_sma.sma_200(stock_symbol, api_key)
                        current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.ema_10_30(stock_symbol, api_key)

                        if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow)): # SELL
                            if buy_id != 0:

                                cross.close_order(buy_id)
                                print('Trade ID:', buy_id, 'Status: CLOSED' + '\n')
                                email('Order Closed - test', str(buy_id), 'Check if order has been closed', 'private')
                                buy_id = 0
                        if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_ema_slow > current_sma200)): # SELL
                            trade_msg(stock_symbol, 'SELL')
                            # email('SELL', stock_symbol, email_message)
                            email('SELL - test', stock_symbol, email_message, 'private')
                            sell_id = cross.create_order('CROSS', 'SELL')
                            break
                        elif ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_ema_slow < current_sma200)): # breakout
                            break

                    except Exception as e :
                        exception_alert(e)
                        email('TEST BOT: EXCEPTION ERROR -', 'INNER LOOP', (str(traceback.format_exc()) + '\n' + str(e)), 'private')
                        time.sleep(random.randint(60, 150))

                    time.sleep(540)

            if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow) and (current_ema_slow > current_sma200)): # SELL
                trade_msg(stock_symbol, 'SELL')
                # email('SELL', stock_symbol, email_message)
                email('SELL - test', stock_symbol, email_message, 'private')
                if buy_id != 0:
                    cross.close_order(buy_id)
                    print('Trade ID:', buy_id, 'Status: CLOSED' + '\n')
                    email('Order Closed - test', str(buy_id), 'Check if order has been closed', 'private')
                    buy_id = 0
                sell_id = cross.create_order('CROSS', 'SELL')

                while True:
                    time.sleep(60)
                    try:
                        current_sma200 = ema_sma.sma_200(stock_symbol, api_key)
                        current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.ema_10_30(stock_symbol, api_key)

                        if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow)):  # BUY
                            if sell_id != 0:
                                cross.close_order(sell_id)
                                print('Trade ID:', sell_id, 'Status: CLOSED' + '\n')
                                email('Order Closed - test', str(sell_id), 'Check if order has been closed', 'private')
                                sell_id = 0
                        if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_ema_slow < current_sma200)):  # BUY
                            trade_msg(stock_symbol, 'BUY')
                            # email('BUY', stock_symbol, email_message)
                            email('BUY - test', stock_symbol, email_message, 'private')
                            buy_id = cross.create_order('CROSS', 'BUY')

                            break
                        elif ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow) and (current_ema_slow > current_sma200)): # breakout

                    except Exception as e :
                        exception_alert(e)
                        email('TEST BOT: EXCEPTION ERROR -', 'INNER LOOP', (str(traceback.format_exc()) + '\n' + str(e)), 'private')
                        time.sleep(random.randint(60, 150))

                    time.sleep(540)

        except Exception as e :
            exception_alert(e)
            email('TEST BOT: EXCEPTION', 'ERROR', (str(traceback.format_exc()) + '\n' + str(e)), 'private')
            time.sleep(random.randint(60, 150))

        time.sleep(600)
