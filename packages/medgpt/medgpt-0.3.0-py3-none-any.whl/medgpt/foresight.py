import torch.nn as nn

class Foresight(object):
    def __init__(self, tokenizer, device, model, cdb=None):
        self.tokenizer = tokenizer
        self.device = device
        self.model = model
        self.cdb = cdb

    def mcq(self, question, options, tkn2id, do_print=False):
        option2p = {}
        q_data = self.tokenizer(question, return_tensors=True, device=self.device)
        logits = model.forward(**q_data)
        smax = nn.Softmax(dim=0)

        ps = sm(logits[0, -1, :]).detach().cpu().numpy()

        for option in options:
            tkn_id = tkn2id[option]
            option2p[option] = {'original': ps[tkn_id]}

        p_sum = sum([v['original'] for v in option2p.values()])

        for option in options:
            tkn_id = tkn2id[option]
            option2p[opton]['norm'] = ps[tkn_id] / p_sum

        if do_print:
            for option in options:
                print("{:30} - {:.2f} - {:.2f}".format(option[:30],
                                                       option2p[option['original'],
                                                       option2p[option['norm']))


        return option2p
