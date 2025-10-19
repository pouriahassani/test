
// This is free and unencumbered software released into the public domain.

// #include "util.h"
// The main function has to be called my_main. An explanation will follow.
#include <math.h>
#include <stdio.h>
#include "file_io.h"
#include "newlib_stubs.h"

// #include <stdlib.h>
void my_main()
{
    // There are a few print functions located in util.h (found in dir _libs).
    // Contrary to printf there is a function for each type and should always
    // end with a newline as this tells the system the message is complete.
    
    // Please note that these prints can increase the program size dramatically
    // and it is best to use as few characters as possible e.g. using "s"
    // instead of "start" and "d" instead of "done".
    
    // The messeges are detected by the debugger module and further processed
    // by the simulation environment (sim_main.cpp under configurations)
    float x = 0;
    // float Z[100]  ={
        // 1196.093994, 3506.360107, 2564.884033, 4381.979004, 34.449600, 3853.311768, 1168.934937, 2430.388916, 5917.436035, 6738.983887, 
        // 102.748398, 7710.552246, 9.578700, 778.939209, 5872.217285, 293.431580, 2362.247314, 1166.668701, 5428.461426, 5309.015625, 
        // 390.833588, 3190.776611, 8738.637695, 518.982117, 1644.200562, 791.047485, 2599.258057, 7453.602051, 5070.031738, 2613.386475, 
        // 1920.625000, 1.124900, 5983.667969, 195.977509, 4599.901855, 6669.090820, 374.802429, 2924.850342, 5437.977539, 7046.015625, 
        // 2894.351074, 926.320923, 5922.505371, 2084.094482, 1930.226929, 1731.599976, 270.190491, 5325.409668, 2634.191406, 358.307983, 
        // 2693.372070, 1670.492798, 283.518036, 1405.970947, 4412.210449, 5557.860352, 698.002502, 139.544601, 1107.507446, 1945.551880, 
        // 2303.460938, 5056.374512, 1119.604004, 340.011078, 1643.737427, 7935.841309, 282.076202, 1235.864136, 2239.131104, 951.231628, 
        // 1367.062500, 2419.536865, 3647.086670, 2766.733887, 4258.647461, 5266.007324, 6865.233398, 3362.021240, 8612.939453, 526.161804, 
        // 4081.352295, 2455.466309, 4397.880371, 66.081497, 1434.711548, 71.751801, 4083.386963, 6493.902832, 1402.974243, 362.773376, 
        // 6580.446289, 2025.898682, 4368.429199, 1460.545166, 3973.984131, 382.043579, 2798.750977, 52.941601, 1079.694092, 2674.295410};
    // ~ print_str( "mul s\n" );
    // for(int i=0;i<100;i++){
        //  x =  Z[99-i]/Z[i];
    //    
        // x = x * ((rand()%10000));
        // display_print(0,0,"\n");
        // display_print(2,i,"");
        // display_print(0,0,"\t");
        // display_print_float(Z[99-i]);
        // display_print(0,0,"\t");
        // display_print_float(x);
    // }
    int a = 333;
    int b = 444;
    
    int pro;
     pro = a * b;
     x = 5.9;
    float y = 12.9;
    float z = cos(x);
    float k = x/y;
    printf("\nz: %f",z);;
    printf("\nk: %f",k);
    printf("\npro: %d",pro);
    printf("\ny %f",y);
    // Debug atan step by step
    void debug_atan_simple();
    debug_atan_simple();
    double half = 0.5;
    double pi = 4*atan(half);
    printf("\npi %f",pi);
    printf("\nEnd of mul program\n");
    // display_print(0,0,"\ny: ");
    // display_print_float(y);
    // display_print(0,0,"\nk: ");
    // display_print_float(k);
    // memmgr_init();
    // float* fptr = (float*)malloc(sizeof(float)*10);
    // fptr[0] = 54.5454;
    // display_print(0,0,"\nfptr[0]: ");
    // display_print_float(fptr[0]*12.5445);

    // // =====================================================
    // // FILE I/O TEST DEMONSTRATION
    // // =====================================================
    // display_print(0,0,"\n\n=== File I/O Test ===\n");

    // // Test 1: Write multiplication results to a file
    // display_print(0,0,"Opening results.txt for write...\n");
    // int write_fd = axe_file_open("results.txt", FILE_MODE_WRITE);
    //  display_print(0,0,"Done results.txt for write...\n");
    //  display_print(2,write_fd,"");
    // if (write_fd >= 0) {
    //     display_print(0,0,"Write file opened successfully!\n");
        
    //     // Write multiplication result
    //     char write_buffer[128];
    //     // Simple integer to string conversion
    //     int temp_pro = pro;
    //     int digits = 0;
    //     int temp = temp_pro;
    //     do { temp /= 10; digits++; } while (temp > 0);
        
    //     write_buffer[0] = 'R'; write_buffer[1] = 'e'; write_buffer[2] = 's'; 
    //     write_buffer[3] = 'u'; write_buffer[4] = 'l'; write_buffer[5] = 't';
    //     write_buffer[6] = ':'; write_buffer[7] = ' ';
        
    //     // Convert number to string (simple implementation)
    //     int pos = 8;
    //     temp = temp_pro;
    //     for (int i = digits - 1; i >= 0; i--) {
    //         int digit_val = 1;
    //         for (int j = 0; j < i; j++) digit_val *= 10;
    //         write_buffer[pos++] = '0' + (temp / digit_val);
    //         temp %= digit_val;
    //     }
    //     write_buffer[pos++] = '\n';
    //     write_buffer[pos] = '\0';
        
    //     int bytes_written = axe_file_write(write_fd, write_buffer, pos);
    //     display_print(0,0,"Bytes written: ");
    //     display_print(2, bytes_written, "");
    //     display_print(0,0,"\n");
        
    //     axe_file_close(write_fd);
    //     display_print(0,0,"Write file closed.\n");
    // } else {
    //     display_print(0,0,"Failed to open write file!\n");
    // }
    //     // Test 3: Read back the data we just wrote
    // display_print(0,0,"Reading back results.txt...\n");
    // int read_fd = axe_file_open("results.txt", FILE_MODE_READ);
    // if (read_fd >= 0) {
    //     display_print(0,0,"Read file opened successfully!\n");
        
    //     char read_buffer[256];
    //     int bytes_read = axe_file_read(read_fd, read_buffer, sizeof(read_buffer) - 1);
    //     read_buffer[bytes_read] = '\0';  // Null terminate
    //     char *buffer_string = read_buffer;
    //     display_print(0,0,"Bytes read: ");
    //     display_print(2, bytes_read, "");
    //     display_print(0,0,"\nFile contents:\n");
    //     display_print(0,0,buffer_string);
        
    //     axe_file_close(read_fd);
    //     display_print(0,0,"Read file closed.\n");
    // } else {
    //     display_print(0,0,"Failed to open read file!\n");
    // }



    // // Test 1: Write multiplication results to a file
    // display_print(0,0,"Opening testdata.txt for write...\n");
    //     write_fd = axe_file_open("testdata.txt", FILE_MODE_WRITE);

    //  display_print(0,0,"Done testdata.txt for write...\n");
    //  display_print(2,write_fd,"");
    // if (write_fd >= 0) {
    //     display_print(0,0,"Write file opened successfully!\n");
        
    //     // Write multiplication result
    //     char write_buffer[128];
    //     // Simple integer to string conversion
    //     int temp_pro = pro;
    //     int digits = 0;
    //     int temp = temp_pro;
    //     do { temp /= 10; digits++; } while (temp > 0);
        
    //     write_buffer[0] = 'R'; write_buffer[1] = 'e'; write_buffer[2] = 's'; 
    //     write_buffer[3] = 'u'; write_buffer[4] = 'l'; write_buffer[5] = 't';
    //     write_buffer[6] = ':'; write_buffer[7] = ' ';
        
    //     // Convert number to string (simple implementation)
    //     int pos = 8;
    //     temp = temp_pro;
    //     for (int i = digits - 1; i >= 0; i--) {
    //         int digit_val = 1;
    //         for (int j = 0; j < i; j++) digit_val *= 10;
    //         write_buffer[pos++] = '0' + (temp / digit_val);
    //         temp %= digit_val;
    //     }
    //     write_buffer[pos++] = '\n';
    //     write_buffer[pos] = '\0';
        
    //     int bytes_written = axe_file_write(write_fd, write_buffer, pos);
    //     display_print(0,0,"Bytes written: ");
    //     display_print(2, bytes_written, "");
    //     display_print(0,0,"\n");
        
    //     axe_file_close(write_fd);
    //     display_print(0,0,"Write file closed.\n");
    // } else {
    //     display_print(0,0,"Failed to open write file!\n");
    // }
    // // // Test 2: Create and write test data
    // // display_print(0,0,"Creating testdata.txt...\n");
    // // int data_fd = axe_file_open("testdata.txt", FILE_MODE_WRITE);
    // // display_print(0,0,"test_data.txt created with fd: ");
    // // // display_print(2, data_fd, "");
    // // display_print(0,0,"\n");
    // // if (data_fd >= 0) {
    // //     display_print(0,0,"Test data file opened successfully!\n");
    // //     // Write some test multiplication data
    // //     char data[] = "Multiplication Test Data:\n333 * 444 = 147852\nFloat: 5.9 / 12.9 = 0.457\nMemory test passed\n";
    // //     axe_file_write(data_fd, data, sizeof(data) - 1);
    // //     axe_file_close(data_fd);
    // //     display_print(0,0,"Test data written successfully.\n");
    // // }
    
    // // // Test 3: Read back the data we just wrote
    // // display_print(0,0,"Reading back test_data.txt...\n");
    // // int read_fd = axe_file_open("test_data.txt", FILE_MODE_READ);
    // // if (read_fd >= 0) {
    // //     display_print(0,0,"Read file opened successfully!\n");
        
    // //     char read_buffer[256];
    // //     int bytes_read = axe_file_read(read_fd, read_buffer, sizeof(read_buffer) - 1);
    // //     read_buffer[bytes_read] = '\0';  // Null terminate
        
    // //     display_print(0,0,"Bytes read: ");
    // //     display_print(2, bytes_read, "");
    // //     display_print(0,0,"\nFile contents:\n");
    // //     display_print(0,0,read_buffer);
        
    // //     axe_file_close(read_fd);
    // //     display_print(0,0,"Read file closed.\n");
    // // } else {
    // //     display_print(0,0,"Failed to open read file!\n");
    // // }
    
    // // // Test 4: Multi-file operation test
    // // display_print(0,0,"Testing multiple file operations...\n");
    // // int file1 = axe_file_open("file1.txt", FILE_MODE_WRITE);
    // // int file2 = axe_file_open("file2.txt", FILE_MODE_WRITE);
    
    // // if (file1 >= 0 && file2 >= 0) {
    // //     display_print(0,0,"Both files opened successfully!\n");
        
    // //     char msg1[] = "This is file 1 content\n";
    // //     char msg2[] = "This is file 2 content\n";
        
    // //     axe_file_write(file1, msg1, sizeof(msg1) - 1);
    // //     axe_file_write(file2, msg2, sizeof(msg2) - 1);
        
    // //     axe_file_close(file1);
    // //     axe_file_close(file2);
        
    // //     display_print(0,0,"Multi-file test completed!\n");
    // // } else {
    // //     display_print(0,0,"Multi-file test failed!\n");
    // //     if (file1 >= 0) axe_file_close(file1);
    // //     if (file2 >= 0) axe_file_close(file2);
    // // }
    
    // // // Test 5: Read from pre-existing input file
    // // display_print(0,0,"Testing input file reading...\n");
    // // int input_fd = axe_file_open("input_test.txt", FILE_MODE_READ);
    // // if (input_fd >= 0) {
    // //     display_print(0,0,"Input file opened successfully!\n");
        
    // //     char input_buffer[256];
    // //     int input_bytes = axe_file_read(input_fd, input_buffer, sizeof(input_buffer) - 1);
    // //     input_buffer[input_bytes] = '\0';
        
    // //     display_print(0,0,"Input file contents:\n");
    // //     display_print(0,0,input_buffer);
    // //     display_print(0,0,"\n");
        
    // //     axe_file_close(input_fd);
    // //     display_print(0,0,"Input file test completed.\n");
    // // } else {
    // //     display_print(0,0,"Input file not found (expected in simulation working directory).\n");
    // // }
    
    // // display_print(0,0,"=== File I/O Test Complete ===\n\n");
    
    // // Original test output
    // // Printing a decimal number. Note the function nl() to print just a newline
    // // right after it.
    
    // //~ print_dec(pro);
    // //~ nl();
    
    // //~ print_str( "mul d\n" );
}
