<?php

namespace Pveltrop\PyRunner;

use Illuminate\Console\Command;

class GUI extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */

    protected $signature = 'pyrunner:gui';

    /**
     * The console command description.
     *
     * @var string
     */

    protected $description = 'Runs PyRunner GUI.';

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

        $cmd = 'python vendor/pveltrop/pyrunner/gui.py';
        exec($cmd, $output, $return);
        if ($return != 0) {
            $cmd = 'python3 vendor/pveltrop/pyrunner/gui.py';
            exec($cmd, $output, $returnTwo);
            if ($returnTwo != 0){
                $console->error('Can\'t launch the GUI. Make sure Tkinter and Python are installed.');
            }
        }
    }
}
