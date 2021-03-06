<?php

namespace Pveltrop\PyRunner;

use Illuminate\Console\Command;

class Start extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */

    protected $signature = 'pyrunner:start {--dev} {--debug} {--shell} {--screenshots}';

    /**
     * The console command description.
     *
     * @var string
     */

    protected $description = 'Launches PyRunner.';

    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct()
    {
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return mixed
     */

    public function handle()
    {
        $console = $this;
        $console->info('Starting PyRunner.');

        $env = ($console->option('env')) ? '--env='.$console->option('env') : '';
        $dev = ($console->option('dev')) ? '--dev' : '';
        $debug = ($console->option('debug')) ? '--debug' : '';
        $shell = ($console->option('shell')) ? '--shell' : '';
        $screenshots = ($console->option('screenshots')) ? '--screenshots' : '';

        $cmd = "gnome-terminal -e 'bash -c \"python vendor/pveltrop/pyrunner/test_app.py ".$dev." ".$debug." ".$shell." ".$screenshots.";bash\"'";
        exec($cmd, $output, $return);
        if ($return != 0) {
            $cmd = "gnome-terminal -e 'bash -c \"python3 vendor/pveltrop/pyrunner/test_app.py ".$dev." ".$debug." ".$shell." ".$screenshots.";bash\"'";
            exec($cmd, $output, $returnTwo);
            if ($returnTwo != 0){
                $cmd = 'start "test" cmd.exe /k "python vendor/pveltrop/pyrunner/test_app.py '.$dev.' '.$debug.' '.$shell.' '.$screenshots.'"';
                exec($cmd, $output, $return);
                if ($return != 0) {
                    $cmd = 'start "test" cmd.exe /k "python3 vendor/pveltrop/pyrunner/test_app.py '.$dev.' '.$debug.' '.$shell.' '.$screenshots.'"';
                    exec($cmd, $output, $returnTwo);
                    if ($returnTwo != 0){
                        $console->error('Can\'t launch PyRunner.');
                    }
                }
            }
        }
        
    }
}
