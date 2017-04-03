from . import Handler
from app.params import *


class Polarizer(Handler):
    def make(self, base=None):
        raise NotImplementedError()

    def fetch(self):
        pass

    def restart(self):
        raise NotImplementedError()

    def abandon(self):
        raise NotImplementedError()

    def submit(self):
        self.make_files()
        self.upload_files()
        self.submit_job('single')

        self.set_status(self.STATE_SUBMITTED)

    def pull(self):
        raise NotImplementedError()

    def rate(self):
        raise NotImplementedError()

    def set_status(self, status):
        pass

    def make_files(self):
        self.make_meep_files()
        self.make_matlab_files()
        self.make_sbatch_files()

    def make_matlab_files(self):
        self.write_file('matlab.sh', self.render_tpl('matlab', {
            '__MATLAB_NAME__': self.config['matlab']
        }))
        # self.write_file('xy.py', self.render_tpl('xy'))

    def make_sbatch_files(self):
        content = self.render_tpl('sbatch', {
            '__NAME__': self.sample.job_name,
            '__WORKDIR__': self.remote_sample_folder,
            '__ACCOUNT__': SBATCH_ACCOUNT,
            '__PARTITION__': SBATCH_PARTITION,
            '__TIME__': self.config['time']
        })
        self.write_file('sbatch.sh', content)

    def make_meep_files(self):
        pass
        # whole_width = self.config['width']
        # whole_length = self.config['length']
        #
        # l_input = self.config['meep_linput']
        # l_output = self.config['meep_loutput']
        #
        # for min_max in self.TYPES:
        #     header = self.render_tpl('meep-%s-header' % min_max, {
        #         '__PIXEL_LENGTH__': whole_length / 10,
        #         '__PIXEL_WIDTH__': whole_width / 10,
        #         '__GRAPH_LENGTH__': self.config['graphene_length'],
        #         '__RESOLUTION__': RESOLUTION,
        #         '__LAYOUT_LENGTH__': whole_length,
        #         '__LAYOUT_WIDTH__': whole_width,
        #         '__L_INPUT__': l_input,
        #         '__L_OUTPUT__': l_output,
        #         '__INPUT_WAVEGUIDE__': self.config['meep_input_waveguide']
        #     })
        #     points = []
        #
        #     for part_name, part_points in self.sample.parts.items():
        #         part_cfg = self.config['parts'][part_name]
        #         layout = numpy.array(part_points).reshape((part_cfg['width']['size'], part_cfg['length']['size']))
        #
        #         width_offset = part_cfg['width']['offset']
        #         length_offset = part_cfg['length']['offset']
        #
        #         for r in range(0, len(layout)):
        #             row = layout[r]
        #             for c in range(0, len(row)):
        #                 if int(row[c]) == 1:
        #                     points.append(self.render_tpl('meep-point', {
        #                         '__LENGTH_OFFSET__': c + 1 + length_offset,
        #                         '__WIDTH_OFFSET__': r + 1 + width_offset,
        #                     }))
        #
        #     points = "\n\n".join(points)
        #     footer = self.render_tpl('meep-%s-footer' % min_max, {
        #         '__OUTPUT_WAVEGUIDE__': self.config['meep_output_waveguide'],
        #         '__EZ__': self.config['meep_ez']
        #     })
        #     content = header + points + footer
        #     self.write_file('meep-' + min_max + '.ctl', content)
