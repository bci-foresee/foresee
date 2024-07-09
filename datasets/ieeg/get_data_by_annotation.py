import getpass
import argparse

from ieegpy.ieeg.auth import Session
from ieegpy.ieeg.processing import ProcessSlidingWindowPerChannel, ProcessSlidingWindowAcrossChannels


def print_montages(dataset):
    """
    Prints the montages of the dataset (if they exist)
    """
    montages = dataset.montages
    for name, montage_list in montages.items():
        for montage in montage_list:
            print(name, montage.portal_id, montage.pairs)


def print_annotation_types(dataset):
    """
    Prints the valid annotation types for the dataset
    """
    annotation_types = []
    annotation_layers = dataset.get_annotation_layers()
    for name, count in annotation_layers.items():
        annotations = dataset.get_annotations(name)
        for a in annotations:
            if a.type not in annotation_types:
                annotation_types.append(a.type)
    print("Annotation types for {}: ".format(dataset.name))
    for at in annotation_types:
        print(at)


def main():
    """
    Prints requested data
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', required=True, help='username')
    parser.add_argument('-p', '--password',
                        help='password (will be prompted if omitted)')

    parser.add_argument('dataset', help='dataset name')
    parser.add_argument('annotation_type', help='annotation for seizures')

    args = parser.parse_args()

    if not args.password:
        args.password = getpass.getpass()

    with Session(args.user, args.password) as session:
        dataset_name = args.dataset
        dataset = session.open_dataset(dataset_name)

        print_montages(dataset)
        print_annotation_types(dataset)
        channels = list(range(len(dataset.ch_labels)))

        print("Reading data for {}:".format(args.annotation_type))
        annotation_layers = dataset.get_annotation_layers()
        for name, count in annotation_layers.items():
            annotations = dataset.get_annotations(name)
            for a in annotations:
                if a.type == args.annotation_type:
                    start_time = a.start_time_offset_usec
                    end_time = a.end_time_offset_usec
                    raw_data = dataset.get_data(start_time, end_time - start_time, channels)
        
        print(raw_data.shape)
        print(raw_data[0].shape)
        print(raw_data[:][0])

        session.close_dataset(dataset_name)


if __name__ == "__main__":
    main()
