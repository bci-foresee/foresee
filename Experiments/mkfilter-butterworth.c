
// ----------- (0.1, 4) band ----------------

/* Digital filter designed by mkfilter/mkshape/gencode   A.J. Fisher
   Command line: ./mkfilter -Bu -Bp -o 5 -a 0.00025 0.01 -l */

#define NZEROS 10
#define NPOLES 10
#define GAIN   5.890713166e+08

static float xv[NZEROS+1], yv[NPOLES+1];

static void filterloop()
  { for (;;)
      { xv[0] = xv[1]; xv[1] = xv[2]; xv[2] = xv[3]; xv[3] = xv[4]; xv[4] = xv[5]; xv[5] = xv[6]; xv[6] = xv[7]; xv[7] = xv[8]; xv[8] = xv[9]; xv[9] = xv[10]; 
        xv[10] = 'next input value' / GAIN;
        yv[0] = yv[1]; yv[1] = yv[2]; yv[2] = yv[3]; yv[3] = yv[4]; yv[4] = yv[5]; yv[5] = yv[6]; yv[6] = yv[7]; yv[7] = yv[8]; yv[8] = yv[9]; yv[9] = yv[10]; 
        yv[10] =   (xv[10] - xv[0]) + 5 * (xv[2] - xv[8]) + 10 * (xv[6] - xv[4])
                     + ( -0.8201374968 * yv[0]) + (  8.3635427995 * yv[1])
                     + (-38.3822761210 * yv[2]) + (104.3882390000 * yv[3])
                     + (-186.3227066700 * yv[4]) + (228.0589411300 * yv[5])
                     + (-193.8606607400 * yv[6]) + (113.0053670900 * yv[7])
                     + (-43.2315892410 * yv[8]) + (  9.8012802461 * yv[9]);
        'next output value' = yv[10];
      }
  }


// ----------- (4,8) band ----------------

/* Digital filter designed by mkfilter/mkshape/gencode   A.J. Fisher
   Command line: ./mkfilter -Bu -Bp -o 5 -a 0.01 0.02 -l */

#define NZEROS 10
#define NPOLES 10
#define GAIN   3.616929452e+07

static float xv[NZEROS+1], yv[NPOLES+1];

static void filterloop()
  { for (;;)
      { xv[0] = xv[1]; xv[1] = xv[2]; xv[2] = xv[3]; xv[3] = xv[4]; xv[4] = xv[5]; xv[5] = xv[6]; xv[6] = xv[7]; xv[7] = xv[8]; xv[8] = xv[9]; xv[9] = xv[10]; 
        xv[10] = 'next input value' / GAIN;
        yv[0] = yv[1]; yv[1] = yv[2]; yv[2] = yv[3]; yv[3] = yv[4]; yv[4] = yv[5]; yv[5] = yv[6]; yv[6] = yv[7]; yv[7] = yv[8]; yv[8] = yv[9]; yv[9] = yv[10]; 
        yv[10] =   (xv[10] - xv[0]) + 5 * (xv[2] - xv[8]) + 10 * (xv[6] - xv[4])
                     + ( -0.8159766800 * yv[0]) + (  8.2928122581 * yv[1])
                     + (-37.9613651660 * yv[2]) + (103.0719262700 * yv[3])
                     + (-183.8272415500 * yv[4]) + (225.0212908000 * yv[5])
                     + (-191.4589373100 * yv[6]) + (111.8076742600 * yv[7])
                     + (-42.8882014600 * yv[8]) + (  9.7580185732 * yv[9]);
        'next output value' = yv[10];
      }
  }

// ----------- (8,12) band ----------------

/* Digital filter designed by mkfilter/mkshape/gencode   A.J. Fisher
   Command line: ./mkfilter -Bu -Bp -o 5 -a 0.02 0.03 -l */

#define NZEROS 10
#define NPOLES 10
#define GAIN   3.611451395e+07

static float xv[NZEROS+1], yv[NPOLES+1];

static void filterloop()
  { for (;;)
      { xv[0] = xv[1]; xv[1] = xv[2]; xv[2] = xv[3]; xv[3] = xv[4]; xv[4] = xv[5]; xv[5] = xv[6]; xv[6] = xv[7]; xv[7] = xv[8]; xv[8] = xv[9]; xv[9] = xv[10]; 
        xv[10] = 'next input value' / GAIN;
        yv[0] = yv[1]; yv[1] = yv[2]; yv[2] = yv[3]; yv[3] = yv[4]; yv[4] = yv[5]; yv[5] = yv[6]; yv[6] = yv[7]; yv[7] = yv[8]; yv[8] = yv[9]; yv[9] = yv[10]; 
        yv[10] =   (xv[10] - xv[0]) + 5 * (xv[2] - xv[8]) + 10 * (xv[6] - xv[4])
                     + ( -0.8159766800 * yv[0]) + (  8.2272267013 * yv[1])
                     + (-37.4301796450 * yv[2]) + (101.1853826500 * yv[3])
                     + (-179.9897686400 * yv[4]) + (220.1314527600 * yv[5])
                     + (-187.4621386000 * yv[6]) + (109.7612297700 * yv[7])
                     + (-42.2880734300 * yv[8]) + (  9.6808451053 * yv[9]);
        'next output value' = yv[10];
      }
  }


// ----------- (12,30) band ----------------

/* Digital filter designed by mkfilter/mkshape/gencode   A.J. Fisher
   Command line: ./mkfilter -Bu -Bp -o 5 -a 0.03 0.075 -l */

#define NZEROS 10
#define NPOLES 10
#define GAIN   2.711202696e+04

static float xv[NZEROS+1], yv[NPOLES+1];

static void filterloop()
  { for (;;)
      { xv[0] = xv[1]; xv[1] = xv[2]; xv[2] = xv[3]; xv[3] = xv[4]; xv[4] = xv[5]; xv[5] = xv[6]; xv[6] = xv[7]; xv[7] = xv[8]; xv[8] = xv[9]; xv[9] = xv[10]; 
        xv[10] = 'next input value' / GAIN;
        yv[0] = yv[1]; yv[1] = yv[2]; yv[2] = yv[3]; yv[3] = yv[4]; yv[4] = yv[5]; yv[5] = yv[6]; yv[6] = yv[7]; yv[7] = yv[8]; yv[8] = yv[9]; yv[9] = yv[10]; 
        yv[10] =   (xv[10] - xv[0]) + 5 * (xv[2] - xv[8]) + 10 * (xv[6] - xv[4])
                     + ( -0.3990100050 * yv[0]) + (  4.1615662713 * yv[1])
                     + (-19.7568686440 * yv[2]) + ( 56.2070319960 * yv[3])
                     + (-106.0979110400 * yv[4]) + (138.8326180500 * yv[5])
                     + (-127.5312431000 * yv[6]) + ( 81.2061196740 * yv[7])
                     + (-34.3049564260 * yv[8]) + (  8.6826497480 * yv[9]);
        'next output value' = yv[10];
      }
  }

// ----------- (30,80) band ----------------

/* Digital filter designed by mkfilter/mkshape/gencode   A.J. Fisher
   Command line: ./mkfilter -Bu -Bp -o 5 -a 0.075 0.2 -l */

#define NZEROS 10
#define NPOLES 10
#define GAIN   3.049509079e+02

static float xv[NZEROS+1], yv[NPOLES+1];

static void filterloop()
  { for (;;)
      { xv[0] = xv[1]; xv[1] = xv[2]; xv[2] = xv[3]; xv[3] = xv[4]; xv[4] = xv[5]; xv[5] = xv[6]; xv[6] = xv[7]; xv[7] = xv[8]; xv[8] = xv[9]; xv[9] = xv[10]; 
        xv[10] = 'next input value' / GAIN;
        yv[0] = yv[1]; yv[1] = yv[2]; yv[2] = yv[3]; yv[3] = yv[4]; yv[4] = yv[5]; yv[5] = yv[6]; yv[6] = yv[7]; yv[7] = yv[8]; yv[8] = yv[9]; yv[9] = yv[10]; 
        yv[10] =   (xv[10] - xv[0]) + 5 * (xv[2] - xv[8]) + 10 * (xv[6] - xv[4])
                     + ( -0.0723156691 * yv[0]) + (  0.6368872577 * yv[1])
                     + ( -2.8198218361 * yv[2]) + (  8.0640603736 * yv[3])
                     + (-16.3818055300 * yv[4]) + ( 24.6025699180 * yv[5])
                     + (-27.6694600560 * yv[6]) + ( 23.0616757780 * yv[7])
                     + (-13.6958889160 * yv[8]) + (  5.2541969233 * yv[9]);
        'next output value' = yv[10];
      }
  }


// ----------- (80,120) band ----------------

/* Digital filter designed by mkfilter/mkshape/gencode   A.J. Fisher
   Command line: ./mkfilter -Bu -Bp -o 5 -a 0.2 0.3 -l */

#define NZEROS 10
#define NPOLES 10
#define GAIN   7.796778047e+02

static float xv[NZEROS+1], yv[NPOLES+1];

static void filterloop()
  { for (;;)
      { xv[0] = xv[1]; xv[1] = xv[2]; xv[2] = xv[3]; xv[3] = xv[4]; xv[4] = xv[5]; xv[5] = xv[6]; xv[6] = xv[7]; xv[7] = xv[8]; xv[8] = xv[9]; xv[9] = xv[10]; 
        xv[10] = 'next input value' / GAIN;
        yv[0] = yv[1]; yv[1] = yv[2]; yv[2] = yv[3]; yv[3] = yv[4]; yv[4] = yv[5]; yv[5] = yv[6]; yv[6] = yv[7]; yv[7] = yv[8]; yv[8] = yv[9]; yv[9] = yv[10]; 
        yv[10] =   (xv[10] - xv[0]) + 5 * (xv[2] - xv[8]) + 10 * (xv[6] - xv[4])
                     + ( -0.1254306222 * yv[0]) + (  0.0000000000 * yv[1])
                     + ( -0.8811300754 * yv[2]) + (  0.0000000000 * yv[3])
                     + ( -2.5452528683 * yv[4]) + (  0.0000000000 * yv[5])
                     + ( -3.8060181193 * yv[6]) + (  0.0000000000 * yv[7])
                     + ( -2.9754221097 * yv[8]) + (  0.0000000000 * yv[9]);
        'next output value' = yv[10];
      }
  }