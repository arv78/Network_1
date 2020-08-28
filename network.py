#stop & w8
#point to point and fixed size framing
# list of seq. nums and we need sn and rn and timer 
# genereate a random number between 1 and 100 to simulate the probability of packet lost (event = Arroival notification)

#Go-back_n
#point to point and fixed size framing
# list of seq. nums and we need sn and sf and rn and timer (sf and sn for window_size which is 2^m -1)
# genereate a random number between 1 and 100 to simulate the probability of packet lost (event = Arroival notification)

#selective-repeat
#point to point and fixed size framing
# list of seq. nums and we need sn and sf and rn and timer (sf and sn for window_size which is 2^(m -1) and receiver window_size = sender)
# genereate a random number between 1 and 100 to simulate the probability of packet lost (event = Arroival notification)

import time
import timeit
import random
# decides if error occures
def random_lost (percentage):
    ls_rand = random.randrange(1,100)
    if (ls_rand < percentage):
        return True
    return False
# wait for ack
def sleep():
    time.sleep(.01)
# transmission delay
def delay():
    time.sleep(.001)

#Stop_and_wait
def Stop_and_wait (number_of_frames,error_percentage):
    # creating sequence number
    sequence_number = []
    sequence_number.append(0)
    for i in range(1,number_of_frames):
        if (sequence_number[i-1] == 0):
            sequence_number.append(1)
        else:
            sequence_number.append(0)
    sn = 0
    rn = 1
    can_send = True
    store_seq = 0
    received = False
    #start sending
    while (sn < len(sequence_number)):

        if (can_send):
            # frame lost
            if (random_lost(error_percentage)):
                received = False
            # frame not lost
            else:
                # transmission delay
                delay()
                can_send = False
                store_seq = sn
                sn += 1
                received = True
        delay()
        if (received):
            # ack not lost
            if (random_lost(error_percentage) == False):
                if (sn == rn):
                    can_send = True
                    # akc(transmission) delay
                    delay()
                    rn += 1
            else:
                # wait for ack (it's lost)
                sleep()
                sn -= 1
                can_send = True

def Go_back_N (number_of_frames,error_percentage):
    sn = 0
    sf = 0
    m = 4
    sw = (2**m)-2
    sequence_number = []
    #creating sequence number
    counter = 0
    for i in range(0,number_of_frames):
        if((2**m)-1 == counter):
            counter=0
        sequence_number.append(counter)
        counter += 1

    rn = 0
    store_seq = 0
    received = True
    frame_lost = False
    #start sending
    while (sf < len(sequence_number)):
        if (sn - sf < sw):
            #frame lost
            if (random_lost(error_percentage)):
                if(sn<len(sequence_number)):
                    sn += 1
                    frame_lost = True
            else:
                # send frame delay
                delay()
                store_seq = sn
                #for last window
                if(sn<len(sequence_number)):
                    sn += 1
                if(sn==len(sequence_number)):
                    frame_lost = False
                if(frame_lost == False):
                    rn += 1
                # ack lost
                if (random_lost(error_percentage)):
                    received = False
                else:
                    # ack (transmission) delay
                    delay()
                    received = True
                    # update sf
                    sf = rn
                
        else:
            # wait for ack
            sleep()
            # resending from the begining of the windows
            sn = sf
            received=True
            frame_lost = False

def selective_repeat(number_of_frames,error_percentage):
    sn = 0
    sf = 0
    m = 4
    sw = 2**(m-1)
    sequence_number = []
    #creating sequence number
    counter = 0
    for i in range(0,number_of_frames):
        if((2**m)-1 == counter):
            counter=0
        sequence_number.append(counter)
        counter += 1

    # to store which frame is sent or lost
    received_list = [False] * sw 
    # pointer of the received_list
    pointer_received = 0
    rn = 0
    received = True
    frame_lost = False
    #start sending
    while (sf < len(sequence_number)):
        if (sn - sf < sw):
            #frame lost
            if (random_lost(error_percentage)):
                if(sn<len(sequence_number)):
                    sn += 1
                    frame_lost = True
                # pointer update
                if(pointer_received<len(received_list)):
                    pointer_received += 1
            else:
                # send frame delay
                delay()
                # for the last window
                if(sn < len(sequence_number)):
                    sn += 1
                if(sn == len(sequence_number)):
                    frame_lost = False
                if(frame_lost == False):
                    rn += 1
                # update received list
                if (frame_lost == True):
                    if(pointer_received<len(received_list)):
                        received_list[pointer_received] = True
                        pointer_received += 1
                # ack lost
                if (random_lost(error_percentage)):
                    received = False
                else:
                    # ack delay
                    delay()
                    received = True
                    sf = rn
                
        else:
            # wait for ack
            sleep()
            for i in range(len(received_list)):
                #print(type(received_list[i]),received_list[i])
                if(received_list[i]):
                    received_list[i] = False
                #resend frame lost
                else:
                    delay()
                    #if frame lost again
                    if(random_lost(error_percentage)):
                        #resend
                        #if ack lost again
                        if(random_lost(error_percentage)):
                            #wait for ack
                            sleep()
                        else:
                            delay()
                        i -= 1
            sf = sn
            rn += sw
            pointer_received = 0
            received = True
            frame_lost = False


def main():
    # input
    frame_size = eval(input ("frame_size: "))
    number_of_recievers = eval(input ("number_of_recievers: "))
    error_percentage = eval(input("error_percentage: "))
    # initial data length
    data_len = 5000 * number_of_recievers
    real_data_len = 5000
    # number of frames
    number_of_frames = data_len // frame_size
    # run time
    start = timeit.default_timer()
    Stop_and_wait(number_of_frames,error_percentage)
    stop = timeit.default_timer()
    # calcualte throughput
    throughput = ( real_data_len) // (stop - start)
    print('Stop_and_wait_Time: ', stop - start, ' sec')
    print('Stop_and_wait_Throughput: ',throughput,' bit/sec')

    # run time
    start = timeit.default_timer()
    Go_back_N(number_of_frames,error_percentage)
    stop = timeit.default_timer()
    # calcualte throughput
    throughput = ( real_data_len) // (stop - start)
    print('Go_back_N_Time: ', stop - start, ' sec')
    print('Go_back_N_Throughput: ',throughput,' bit/sec')

    # run time
    start = timeit.default_timer()
    selective_repeat(number_of_frames,error_percentage)
    stop = timeit.default_timer()
    # calcualte throughput
    throughput = ( real_data_len) // (stop - start)
    print('Selective_repeat_Time: ', stop - start, ' sec')
    print('Selective_repeat_Throughput: ',throughput,' bit/sec')
main()
