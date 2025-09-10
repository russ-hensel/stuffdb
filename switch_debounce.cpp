


>>search tk tc


I would like to make a c++ object for the arduino

the purpose is to debounce an switch on an input  pin.
call this input_pin

to do the debounce the get_input method will skip ignore_cycles_max after
registering any state change

the counter for this will be ix_ignore

the last state detected will be stored in state_last_detect

we will have a method  has_gone_high  which will report true if the input has gone
high if we have detected this during a cycle we did not ignore if we found a high state

 Set up a first round set of code for this with a fairly minimal set of code, I will
make additions in the future


---------------------------------

// SwitchDebouncer.h
#ifndef SWITCH_DEBOUNCER_H
#define SWITCH_DEBOUNCER_H

#include <Arduino.h>

class SwitchDebouncer {
public:
    SwitchDebouncer(uint8_t inputPin, uint8_t ignoreCyclesMax)
        : input_pin(inputPin),
          ignore_cycles_max(ignoreCyclesMax),
          ix_ignore(0),
          state_last_detect(LOW),
          went_high(false)
    {
        pinMode(input_pin, INPUT);
    }

    // Call this every loop() cycle
    void update() {
        if (ix_ignore > 0) {
            ix_ignore--;
            return;
        }

        int current = digitalRead(input_pin);

        if (current != state_last_detect) {
            state_last_detect = current;
            ix_ignore = ignore_cycles_max;

            if (current == HIGH) {
                went_high = true;
            }
        }
    }

    // Returns true if the switch has gone high since last check
    bool has_gone_high() {
        if (went_high) {
            went_high = false;
            return true;
        }
        return false;
    }

private:
    uint8_t input_pin;
    uint8_t ignore_cycles_max;
    uint8_t ix_ignore;
    int state_last_detect;
    bool went_high;
};

#endif


now lets add a bit also have a state went_low

if we

.........


can we do as some sort of state machine


        ix_ignore     went_high    went_low
