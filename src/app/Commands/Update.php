<?php

namespace Pveltrop\PyRunner;

use Illuminate\Console\Command;

class Update extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */

    protected $signature = 'pyrunner:update';

    /**
     * The console command description.
     *
     * @var string
     */

    protected $description = 'Updates PyRunner.';

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
        $console->info('Updating PyRunner.');

        $cmd = 'python vendor/pveltrop/pyrunner/update.py';
        exec($cmd, $output, $return);
        if ($return != 0) {
            $cmd = 'python3 vendor/pveltrop/pyrunner/update.py';
            exec($cmd, $output, $returnTwo);
            if ($returnTwo != 0){
                $console->error('Can\'t launch the update script');
            }
        }
        $console->info('Finished updating');
    }
}
