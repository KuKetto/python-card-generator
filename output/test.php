<?php

include("experimental.php");
include("GeneratedCardDictionaries.php");

function test_card_name_lookup() {
    global $CardSubtypeDict;
    $iterations_so_far = 0;
    $avg_dict_lookup = 0;
    $avg_switch_case_lookup = 0;

    $min_dict_lookup = 10000000;
    $max_dict_lookup = 0;
    $min_switch_case_lookup = 10000000;
    $max_switch_case_lookup = 0;

    foreach($CardSubtypeDict as $key => $value) {
        $dict_lookup_start = hrtime(true);
        GeneratedCardSubtype2($key);
        $dict_lookup_finish = hrtime(true);

        $switch_case_lookup_start = hrtime(true);
        GeneratedCardSubtype($key);
        $switch_case_lookup_finish = hrtime(true);

        $elapsed_dict_lookup_time_ns = $dict_lookup_finish - $dict_lookup_start;
        $elapsed_switch_case_lookup_time_ns = $switch_case_lookup_finish - $switch_case_lookup_start;

        if ($iterations_so_far == 0) {
            $avg_dict_lookup = $elapsed_dict_lookup_time_ns;
            $avg_switch_case_lookup = $elapsed_switch_case_lookup_time_ns;
        } else {
            $avg_dict_lookup = (($avg_dict_lookup * $iterations_so_far) + $elapsed_dict_lookup_time_ns) / ($iterations_so_far + 1);
            $avg_switch_case_lookup = (($avg_switch_case_lookup * $iterations_so_far) + $elapsed_switch_case_lookup_time_ns) / ($iterations_so_far + 1);
        }
        $iterations_so_far += 1;

        if ($elapsed_dict_lookup_time_ns > $max_dict_lookup) $max_dict_lookup = $elapsed_dict_lookup_time_ns;
        if ($elapsed_dict_lookup_time_ns < $min_dict_lookup) $min_dict_lookup = $elapsed_dict_lookup_time_ns;
        if ($elapsed_switch_case_lookup_time_ns > $max_switch_case_lookup) $max_switch_case_lookup = $elapsed_switch_case_lookup_time_ns;
        if ($elapsed_switch_case_lookup_time_ns < $min_switch_case_lookup) $min_switch_case_lookup = $elapsed_switch_case_lookup_time_ns;
    }

    echo "Original implementation: $avg_switch_case_lookup ns\n";
    echo "\tMinimum time: $min_switch_case_lookup ns\n";
    echo "\tMaximum time: $max_switch_case_lookup ns\n";
    echo "Dict-lookup implementation: $avg_dict_lookup ns\n";
    echo "\tMinimum time: $min_dict_lookup ns\n";
    echo "\tMaximum time: $max_dict_lookup ns\n";
}

test_card_name_lookup();

?>